[visit_me](https://test-django.lyskills.com:82/)

1. create service
```
touch /etc/systemd/system/test_django.uwsgi.service
```
```
nano /etc/systemd/system/test_django.uwsgi.service
```
```
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
#ExecStartPre= mkdir -p /run/uwsgi; chown root:test_django /run/uwsgi
ExecStart=/opt/python-venv/test-django3/bin/uwsgi --ini /etc/systemd/system/test_django.uwsgi.ini
# Requires systemd version 211 or newer
RuntimeDirectory=uwsgi
Restart=always
#KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target

```

2. create emperor
```
touch /etc/systemd/system/test_django.uwsgi.ini
```
```
nano /etc/systemd/system/test_django.uwsgi.ini
```
```
[uwsgi]
emperor=/etc/uwsgi/vassals
#protocol=http
uid=root
gid=test_django



logto=/var/log/uwsgi/test_django.log

```

3. create vassals
```
 nano /etc/uwsgi/vassals/test_django.ini
```
```

[uwsgi]

project=djangoForum
base=/home/ser_name/public_html/test-django

master=true
chdir=/home/ser_name/public_html/test-django/blog_posts
module=blog_posts.wsgi:application

#env=DJANGO_SETTINGS_MODULE= LANG=en_US.UTF-8

pidfile=/run/test-django.pid
processes=5                 # number of worker processes

uid=root
#gid=test_django         # if root, uwsgi can drop privileges

harakiri=20               # respawn processes taking more than 20 seconds
max-requests=5000           # respawn processes after serving 5000 requests
vacuum=true                   # clear environment on exit
#home=/opt/python-venv/test-django3/bin/python    # optional path to a virtual environment
daemonize=/var/log/uwsgi/test_django.log

#http=127.0.0.1:8081
#socket=0.0.0.0:8081

http-socket=/run/uwsgi/test_django.sock

plugins = python3

chmod-socket=755
thunder-lock=true
enable-threads=true

```