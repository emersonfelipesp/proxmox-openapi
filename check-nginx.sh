#!/bin/sh
cat /etc/nginx/nginx.conf
echo "--- http.d directory ---"
ls -la /etc/nginx/http.d/ 2>&1 || echo "http.d does not exist"
echo "--- conf.d directory ---"
ls -la /etc/nginx/conf.d/ 2>&1 || echo "conf.d does not exist"
