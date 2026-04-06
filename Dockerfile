# Build dependencies and the app into a virtualenv with uv from the checked-out repo.
FROM python:3.13-alpine AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# build-base ensures C extensions (httptools, uvloop, etc.) can compile if no
# musllinux wheel is available for the target arch.
RUN apk add --no-cache build-base curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Download mkcert in builder layer
ARG MKCERT_VERSION=1.4.4
ARG TARGETARCH
RUN curl -fsSL -o /usr/local/bin/mkcert \
    "https://github.com/FiloSottile/mkcert/releases/download/v${MKCERT_VERSION}/mkcert-v${MKCERT_VERSION}-linux-${TARGETARCH}" \
 && chmod +x /usr/local/bin/mkcert

# Build from the local repository so the image always matches the checked-out commit.
COPY README.md pyproject.toml ./
COPY proxmox_openapi ./proxmox_openapi

RUN uv venv --seed /app/.venv && \
    /app/.venv/bin/python -m pip install --upgrade pip && \
    /app/.venv/bin/pip install '.' && \
    /app/.venv/bin/pip install 'granian>=2.7.0'

# Application tree + venv only (shared by all runtime images).
FROM python:3.13-alpine AS runtime-base

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PORT=8000 \
    PYTHONUNBUFFERED=1 \
    APP_MODULE=proxmox_openapi.main:create_app

# The code in proxmox_openapi uses main:create_app
# It looks like previously APP_MODULE=proxmox_openapi.mock_main:app

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

RUN mkdir -p /app/scripts && chown -R appuser:appgroup /app

EXPOSE 8000

# Default image: raw uvicorn, no proxy, HTTP only. Smallest possible image.
FROM runtime-base AS raw

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:${PORT:-8000}/health || exit 1

CMD ["sh", "-c", "exec uvicorn ${APP_MODULE} --factory --host 0.0.0.0 --port ${PORT:-8000}"]

# nginx image: nginx terminates HTTPS with mkcert certs, proxies to uvicorn on 127.0.0.1:8001.
# Extra SANs: MKCERT_EXTRA_NAMES. Persist CA: CAROOT + volume.
FROM raw AS nginx

USER root

RUN apk add --no-cache \
    nginx \
    supervisor \
    ca-certificates \
    nss-tools \
 && rm -f /etc/nginx/conf.d/default.conf

COPY --from=builder /usr/local/bin/mkcert /usr/local/bin/mkcert
COPY docker/nginx/proxmox-openapi-https.conf.template /etc/proxmox-openapi/nginx-https.conf.template
COPY docker/nginx/proxmox-openapi-map.conf /etc/nginx/http.d/proxmox-openapi-map.conf
COPY docker/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker/supervisor/proxmox-openapi.conf /etc/supervisor/conf.d/proxmox-openapi.conf
COPY docker/entrypoint-nginx.sh /usr/local/bin/docker-entrypoint-nginx.sh

RUN chmod +x /usr/local/bin/docker-entrypoint-nginx.sh \
 && mkdir -p /certs /var/log/supervisor /var/run/supervisor /var/lib/nginx /var/log/nginx /var/run/nginx /etc/nginx/conf.d /etc/nginx/http.d \
 && chown -R appuser:appgroup /certs /var/log/supervisor /var/run/supervisor /etc/proxmox-openapi /etc/supervisor /var/lib/nginx /var/log/nginx /var/run/nginx /etc/nginx/conf.d /etc/nginx/http.d \
 && sed -i 's/user nginx;/#user nginx;/' /etc/nginx/nginx.conf \
 && sed -i 's/pid \/run\/nginx.pid;/pid \/var\/run\/nginx\/nginx.pid;/' /etc/nginx/nginx.conf \
 && sed -i '/^http {/a \    include /etc/nginx/http.d/*.conf;' /etc/nginx/nginx.conf \
 && chmod -R 777 /var/lib/nginx /var/log/nginx /var/run/nginx /etc/nginx/conf.d /etc/nginx/http.d

ENV MKCERT_CERT_DIR=/certs

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider --no-check-certificate https://127.0.0.1:8000/health || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-nginx.sh"]
CMD []

# granian image: granian ASGI server with native TLS via mkcert. No nginx, no supervisor.
# Smaller than the nginx image; single process handles TLS + HTTP/2 + WebSockets.
FROM runtime-base AS granian

USER root

RUN apk add --no-cache \
    ca-certificates \
    nss-tools \
    openssl

COPY --from=builder /usr/local/bin/mkcert /usr/local/bin/mkcert
COPY docker/entrypoint-granian.sh /usr/local/bin/docker-entrypoint-granian.sh

RUN chmod +x /usr/local/bin/docker-entrypoint-granian.sh \
 && mkdir -p /certs \
 && chown -R appuser:appgroup /certs

ENV MKCERT_CERT_DIR=/certs

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider --no-check-certificate https://127.0.0.1:${PORT:-8000}/health || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-granian.sh"]
CMD []

# `docker build .` without --target uses the raw (uvicorn-only) image.
FROM raw
