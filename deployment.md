We need to setup the environment first. I am using ```Centos 7```

1. install python
    1. run
       ```
        yum install build-essential python3-dev && sudo yum install -y epel openssl11-devel
        ```
    3. run
       ```
       wget https://www.sqlite.org/snapshot/sqlite-snapshot-202309111527.tar.gz
       ```
    4.run
       ```
       tar zxvf sqlite-snapshot-202309111527.tar.gz
       ```
    6. use
       ```
        wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
       ```
    7. use
       ```tar -xf Python-3.10.13.tgz
       ```
    8. run
       ```
       cd Python-3.10.13
        ```
    10. ./configure --enable-optimizations
    11. make & sudo make altinstall

2. create virtual env
    1. python3.10 -m venv /opt/python-venv/test-django3
    2. source /opt/python-venv/test-django3/bin/activate
    3. pip install django=4.2
    4. pip install uwsgi

3. run django project
    1. python3.10 manage.py startproject test_project
    2. set domain following envs
        1. ALLOWED_HOSTS
        2. ```
            BASE_DIR = Path(__file__).resolve().parent.parent
            STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
            STATICFILES_DIRS =  [ os.path.join(BASE_DIR,'static')]
            STATIC_URL = "static/"
            ```
    3. python3.10 manage.py collectstatic
    4. setup mysql database
    5. setup logs
        ```
        LOGGING = {
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "filename": "general.log",
                },
            },
        }
        ```
    6. python3.10 manage.py runserver


4. chown -Rv django:nginx project_dir
5. setup uwsgi
    1. create
        ```
            touch /etc/uwsgi/vassals/test_project.ini && \
            nano /etc/uwsgi/vassals/test_project.ini
        ```
    ```
        [uwsgi]
        http = :8000
        socket = /tmp/uwsgi/test_project.sock
        chdir = /home/server_name/public_html/server_folder/test_project/
        pythonpath = /home/server_name/public_html/server_folder/test_project/test_project
        home = /opt/python-venv/test-django3
        module = test_project.wsgi
        uid = django
        gid = nginx
        chmod-socket = 666
        chown-socket = django:nginx
        master = true
        optimize=2
        processes = 10
        thunder-lock = true
        enable-threads = true
        vacuum = true

    ```
    2. nano /etc/systemd/system/uwsgi.service
    ```
        [Unit]
        Description = uWSGI Emperor
        After = syslog.target

        [Service]
        ExecStart = /opt/python-venv/test-django3/bin/uwsgi --ini /etc/uwsgi/test_django_emperor.ini
        ExecStop = kill -INT 'cat /run/wsgi.pid'
        ExecReload = kill -TERM 'cat /run/wsgi.pid'
        Restart = always
        Type = notify
        NotifyAccess = main
        PIDFile = /run/uwsgi.pid

        [Install]
        WantedBy = multi-user.target

    ```
    3.  nano /etc/uwsgi/test_django_emperor.ini
    ```
        [uwsgi]
        emperor = /etc/uwsgi/vassals
        uid = server_name
        gid = nginx
        logto = /var/log/uwsgi/test_project.log
    ```

6. use the followings for debugging
    ```
   systemctl daemon-reload
   systemctl status uwsgi.service
   systemctl restart uwsgi
   ```

7. check if there is something wrong with .sock file
    ```
        uwsgi --socket /tmp/uwsgi/test_project.sock  --module test_project.wsgi --chmod-socket=664 --ini /etc/uwsgi/vassals/test_django.ini
    ```

8. add user to nginx group
    ```
        gpasswd -a django nginx
    ```
9. verify the .sock file
10. install nginx

11.
 1. all server lives inside ```http directive``` in ```nano /etc/nginx/nginx.conf```
 2. create a file inside ```touch /etc/nginx/conf.d/test_project.conf``` All files are automatically imported in nginx.conf
 3. 
```
   upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8000; # for a web port socket (we'll use this first)
}

server {
    listen 81;
     listen [::]:81;
    server_name website_name www.website_name; # Name of server

        client_max_body_size 64M;

        charset utf-8;

        # Error logs paths, make sure these exist!
        access_log  /var/log/nginx/test-django.access.log;
        error_log  /var/log/nginx/test-django.error.log;


        # Django media
        location /assets {
            alias /home/usmansaleem234/public_html/website_name/test_project/assets;

        }
        location = /favicon.ico {
                log_not_found off;
        }

        # Django static
        location /static {
            alias /home/usmansaleem234/public_html/website_name/test_project/static; # path to static folder of you Django project
        }

        # Everything else to Django server
        location / {
            uwsgi_pass unix:/tmp/uwsgi/test_project.sock;
            #uwsgi_pass  django;
            include uwsgi_params;
        }
}
```

12. sudo nginx -s reload
13. systemctl status nginx.service
14. netstat -na|grep LISTEN | grep :81

