#!/bin/bash

cat > /etc/nginx/sites-available/default <<EOF
server {
        listen 80;
        location / {
            proxy_pass http://127.0.0.1:8000;
            include /etc/nginx/proxy_params;
        }
        location /static/ {
          #alias /usr/local/lib/python3.5/site-packages/django/contrib/admin/static/;
          alias /code/static/;
          autoindex on;
        }
}
EOF

nginx -c /etc/nginx/nginx.conf

gunicorn wsgi:application -b 0.0.0.0:8000 --workers=10
