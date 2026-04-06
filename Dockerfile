# Build dependencies and the app into a virtualenv with uv from the checked-out repo.
FROM python:3.13-alpine AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# build-base ensures C extensions (httptools, uvloop, etc.) can compile if no
# musllinux wheel is available for the target arch.
RUN apk add --no-cache build-base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Build from the local repository so the image always matches the checked-out commit.
COPY README.md pyproject.toml ./
COPY proxmox_openapi ./proxmox_openapi

RUN uv venv --seed /app/.venv && \
    /app/.venv/bin/python -m pip install --upgrade pip && \
    /app/.venv/bin/pip install '.'

# Application tree + venv only (shared by all runtime images).
FROM python:3.13-alpine AS runtime-base

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PORT=8000 \
    PYTHONUNBUFFERED=1 \
    APP_MODULE=proxmox_openapi.mock_main:app

COPY --from=builder /app/.venv /app/.venv

RUN mkdir -p /app/scripts

EXPOSE 8000

# Default image: raw uvicorn, no proxy, HTTP only. Smallest possible image.
FROM runtime-base AS raw

CMD ["sh", "-c", "exec uvicorn ${APP_MODULE} --host 0.0.0.0 --port ${PORT:-8000}"]

# nginx image: nginx terminates HTTPS with mkcert certs, proxies to uvicorn on 127.0.0.1:8001.
# Extra SANs: MKCERT_EXTRA_NAMES. Persist CA: CAROOT + volume.
FROM raw AS nginx

ARG MKCERT_VERSION=1.4.4

# TARGETARCH is set automatically by BuildKit (amd64, arm64, etc.)
ARG TARGETARCH

RUN apk add --no-cache \
    nginx \
    supervisor \
    ca-certificates \
    curl \
    nss-tools \
 && rm -f /etc/nginx/conf.d/default.conf \
 && curl -fsSL -o /usr/local/bin/mkcert \
    "https://github.com/FiloSottile/mkcert/releases/download/v${MKCERT_VERSION}/mkcert-v${MKCERT_VERSION}-linux-${TARGETARCH}" \
 && chmod +x /usr/local/bin/mkcert

COPY docker/nginx/proxmox-openapi-https.conf.template /etc/proxmox-openapi/nginx-https.conf.template
COPY docker/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker/supervisor/proxmox-openapi.conf /etc/supervisor/conf.d/proxmox-openapi.conf
COPY docker/entrypoint-nginx.sh /usr/local/bin/docker-entrypoint-nginx.sh
RUN chmod +x /usr/local/bin/docker-entrypoint-nginx.sh

ENV MKCERT_CERT_DIR=/certs

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-nginx.sh"]
CMD []

# granian image: granian ASGI server with native TLS via mkcert. No nginx, no supervisor.
# Smaller than the nginx image; single process handles TLS + HTTP/2 + WebSockets.
FROM runtime-base AS granian

ARG MKCERT_VERSION=1.4.4
ARG TARGETARCH

RUN apk add --no-cache \
    ca-certificates \
    curl \
    nss-tools \
    openssl \
 && /app/.venv/bin/pip install 'granian>=2.7.0' \
 && curl -fsSL -o /usr/local/bin/mkcert \
    "https://github.com/FiloSottile/mkcert/releases/download/v${MKCERT_VERSION}/mkcert-v${MKCERT_VERSION}-linux-${TARGETARCH}" \
 && chmod +x /usr/local/bin/mkcert

COPY docker/entrypoint-granian.sh /usr/local/bin/docker-entrypoint-granian.sh
RUN chmod +x /usr/local/bin/docker-entrypoint-granian.sh

ENV MKCERT_CERT_DIR=/certs

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-granian.sh"]
CMD []

# `docker build .` without --target uses the raw (uvicorn-only) image.
FROM raw
