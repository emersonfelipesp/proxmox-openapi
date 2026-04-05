ARG APP_MODULE=proxmox_openapi.main:app

FROM python:3.13-slim-bookworm AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY README.md pyproject.toml ./
COPY proxmox_openapi ./proxmox_openapi

RUN uv venv --seed /app/.venv && \
    /app/.venv/bin/python -m pip install --upgrade pip && \
    /app/.venv/bin/pip install '.[playwright]'

FROM python:3.13-slim-bookworm AS runtime-base

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV PATH="/app/.venv/bin:$PATH" \
    PORT=8000 \
    PYTHONUNBUFFERED=1

COPY --from=builder /app/.venv /app/.venv

EXPOSE 8000

FROM runtime-base AS runtime

ARG APP_MODULE

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /etc/nginx/sites-enabled/default \
  && rm -f /etc/nginx/conf.d/default.conf

COPY docker/nginx/proxmox-openapi-http.conf.template /etc/proxmox-openapi/nginx-http.conf.template
COPY docker/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker/supervisor/proxmox-openapi.conf /etc/supervisor/conf.d/proxmox-openapi.conf
COPY docker/entrypoint-runtime.sh /usr/local/bin/docker-entrypoint-runtime.sh
RUN chmod +x /usr/local/bin/docker-entrypoint-runtime.sh

ENV APP_MODULE=${APP_MODULE}

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-runtime.sh"]
CMD []

FROM runtime AS mkcert

ARG MKCERT_VERSION=1.4.4

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    libnss3-tools \
  && rm -rf /var/lib/apt/lists/* \
  && ARCH=$(dpkg --print-architecture) \
  && curl -fsSL -o /usr/local/bin/mkcert \
    "https://github.com/FiloSottile/mkcert/releases/download/v${MKCERT_VERSION}/mkcert-v${MKCERT_VERSION}-linux-${ARCH}" \
  && chmod +x /usr/local/bin/mkcert

COPY docker/nginx/proxmox-openapi-https.conf.template /etc/proxmox-openapi/nginx-https.conf.template
COPY docker/entrypoint-mkcert.sh /usr/local/bin/docker-entrypoint-mkcert.sh
RUN chmod +x /usr/local/bin/docker-entrypoint-mkcert.sh

ENV MKCERT_CERT_DIR=/certs

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-mkcert.sh"]

FROM runtime
