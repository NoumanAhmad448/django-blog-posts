### Deployment using Gunicorn, unicorn and supervisor with nginx
[visit_me](https://fastapi.lyskills.com/)

1. create a service and place it whereever you want
```
touch /home/usr/scripts/fastapi.lyskills.com
```

```
nano /home/usr/scripts/fastapi.lyskills.com
```

```
#!/bin/bash

NAME=fastapi-app
DIR=/home/usmansaleem234/public_html/test-django/blog_posts/fast_api
USER=root
#GROUP=fastapi-user
WORKERS=3
WORKER_CLASS=uvicorn.workers.UvicornWorker

VEN_ENV=/opt/python-venv/test-django3
VENV=$VEN_ENV/bin/activate

BIND=unix:/run/fastapi.lyskills.com.sock
LOG_LEVEL=error

cd $DIR
source $VENV

exec /opt/python-venv/test-django3/bin/gunicorn  main:app \
  --name $NAME \
  --workers $WORKERS \
  --worker-class $WORKER_CLASS \
  --user=$USER \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=/var/log/scripts/fastapi.lyskills.com.log

```

```
chmod u+x /home/usr/scripts/fastapi.lyskills.com
```
test if the above command works using
```
/home/usr/scripts/fastapi.lyskills.com
```
2. install supervisor(centos)
```
yum install supervisor
```
```
easy_install supervisor
```
```
mkdir -p /etc/supervisor/conf.d
```
```
nano /etc/supervisor.conf
```
add at then end of file
```
[include]
files = /etc/supervisor/conf.d/*.conf
```
3. add configuration in supervisor
```
nano /etc/supervisor/conf.d/fastapi.lyskills.com.conf
```
```
[program:fastapi]
command=/home/usmansaleem234/scripts/fastapi.lyskills.com
user=root
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/etc/supervisord.d/fastapi.lyskills.com.log

```
run
```
systemctl enable supervisord

```
```
systemctl start supervisord
```
```
supervisorctl start fastapi
```
```
supervisorctl status fastapi

```
```
curl --unix-socket /run/fastapi.lyskills.com.sock localhost
```

4. nginx configuration
```
upstream app_server {
    server unix:sock_path fail_timeout=0;
}

server {
    listen 83 ssl;
     listen [::]:83 ssl;
    server_name fastapi.lyskills.com www.fastapi.lyskills.com; # Name of server
    ssl_certificate     /etc/ssl/certs/fastapi.lyskills.com.crt;
    ssl_certificate_key /etc/ssl/certs/fastapi.lyskills.com.key;

    if ( $host ~ ^www\.(.+)$ ){
        set $without_www $1;
        rewrite ^ $scheme://$without_www$uri permanent;
    }
    # redirect http to https
    error_page 497 https://$server_name:$server_port$request_uri;

    client_max_body_size 64M;

    charset utf-8;

    # Error logs paths, make sure these exist!
    access_log  /var/log/nginx/fastapi.lyskills.com.access.log;
    error_log  /var/log/nginx/fastapi.lyskills.com.error.log;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        if (!-f $request_filename) {
            proxy_pass http://app_server;
            break;
        }
	}
}
```