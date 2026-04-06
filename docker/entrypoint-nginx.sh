#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

CERT_DIR="${MKCERT_CERT_DIR:-/certs}"
mkdir -p "$CERT_DIR"

mkcert -install

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
printf '%s\n' localhost 127.0.0.1 > "$tmp"
if [ -n "${MKCERT_EXTRA_NAMES:-}" ]; then
  echo "$MKCERT_EXTRA_NAMES" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | grep -v '^$' >> "$tmp"
  echo "$MKCERT_EXTRA_NAMES" | tr ' ' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | grep -v '^$' >> "$tmp"
fi

list=$(sort -u "$tmp" | tr '\n' ' ')

# shellcheck disable=SC2086
mkcert -cert-file "$CERT_DIR/cert.pem" -key-file "$CERT_DIR/key.pem" $list

chmod 644 "$CERT_DIR/cert.pem" 2>/dev/null || true
chgrp nginx "$CERT_DIR/key.pem" 2>/dev/null || true
chmod 640 "$CERT_DIR/key.pem" 2>/dev/null || true

PORT="${PORT:-8000}"

CERT_ESC=$(echo "$CERT_DIR/cert.pem" | sed 's/[\/&]/\\&/g')
KEY_ESC=$(echo "$CERT_DIR/key.pem" | sed 's/[\/&]/\\&/g')
sed -e "s/__PORT__/${PORT}/g" \
    -e "s|__CERT__|${CERT_ESC}|g" \
    -e "s|__KEY__|${KEY_ESC}|g" \
  /etc/proxmox-openapi/nginx-https.conf.template > /etc/nginx/conf.d/proxmox-openapi.conf

exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
