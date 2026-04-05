#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

PORT="${PORT:-8000}"

# Check if the port is already in use
if command -v ss >/dev/null 2>&1; then
    if ss -tuln 2>/dev/null | grep -q ":${PORT} "; then
        echo "ERROR: Port ${PORT} is already in use. Please use another port by setting the PORT environment variable." >&2
        echo "Example: docker run -e PORT=8001 ..." >&2
        exit 1
    fi
elif command -v netstat >/dev/null 2>&1; then
    if netstat -tuln 2>/dev/null | grep -q ":${PORT} "; then
        echo "ERROR: Port ${PORT} is already in use. Please use another port by setting the PORT environment variable." >&2
        echo "Example: docker run -e PORT=8001 ..." >&2
        exit 1
    fi
fi

sed -e "s/__PORT__/${PORT}/g" /etc/proxmox-openapi/nginx-http.conf.template > /etc/nginx/conf.d/proxmox-openapi.conf
exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
