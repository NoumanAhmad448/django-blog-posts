We need to setup the environment first. I am using ```Centos 7```
### Please make sure to create following files on server before auto deployment
1. .env
2. settings.py
3. server_deploy.sh

1. install python
    1. run
       ```
        yum install build-essential python3-dev && sudo yum install -y epel openssl11-devel
        ```
    2. run
       ```
       wget https://www.sqlite.org/snapshot/sqlite-snapshot-202309111527.tar.gz
       ```
    3. run
       ```
       tar zxvf sqlite-snapshot-202309111527.tar.gz
       ```
    4. use
       ```
        wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
       ```
    5. use
       ```
       tar -xf Python-3.10.13.tgz
       ```
    6. run
       ```
       cd Python-3.10.13
        ```
    7. copy
        ```
            ./configure --enable-optimizations
        ```
    8. copy
        ```
         make & sudo make altinstall
        ```

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
5. install postgre
    1. follow guide from postgre officila site to install postgre.
    2. common commands to setup database and create a user account
       1. Enter
    ```
    sudo su postgres || psql
    ```
    2. pass change
    ```
    ALTER USER postgres WITH PASSWORD 'new_pass';
    ```
    3. list users and db
    ```
    \l
    ```
    4. permissions
    ```
    GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO wiki;
    ```
    ```
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO wiki;
    ```
    ```
     ALTER DATABASE test OWNER TO wiki;
    ```
6. setup uwsgi or gunicorn
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

7. use the followings for debugging
    ```
   systemctl daemon-reload
   systemctl status uwsgi.service
   systemctl restart uwsgi
   ```

8. touch /etc/systemd/system/gunicorn.service:
    i. install gunicorn using
    ```
    pip install gunicorn
    ```
     in virtual env and copy
    ```
           [Unit]
        Description=gunicorn daemon
        Requires=test_django.socket #needs to be changed
        After=network.target

        [Service]
        Type=notify
        # the specific user that our service will run as
        User=www-data #user who can access the .sock file in /run/.sock
        #Group=someuser
        # another option for an even more restricted service is
        # DynamicUser=yes
        # see http://0pointer.net/blog/dynamic-users-with-systemd.html
        RuntimeDirectory=mysite
        WorkingDirectory= cd /home/usmansaleem234/public_html/test-django/mysite/mysite #project directory path that does not include                     # manage.py
        ExecStart=/opt/python-venv/test-django3/bin/gunicorn -b 0.0.0.0:8080 blog_posts.wsgi:application
        # fetch gunicorn path using whereis gunicorn
        ExecReload=/bin/kill -s HUP $MAINPID
        KillMode=mixed
        TimeoutStopSec=5
        PrivateTmp=true

        [Install]
        WantedBy=multi-user.target
   ```
    ii. run
    ```
          touch /etc/systemd/system/test_django.socket
    ```
    ```
          nano /etc/systemd/system/test_django.socket
    ```
     and copy
   ```
        [Socket]
        ListenStream=/run/test_django.sock
        # Our service won't need permissions for the socket, since it
        # inherits the file descriptor by socket activation
        # only the nginx daemon will need access to the socket
        SocketUser=www-data #socket user
        # Optionally restrict the socket permissions even more.
        # SocketMode=600

        [Install]
        WantedBy=sockets.target
   ```


9. [uwsgi] check if there is something wrong with .sock file
    1. test project
    ```
        uwsgi --socket /tmp/uwsgi/test_project.sock  --module test_project.wsgi --chmod-socket=664 --ini /etc/uwsgi/vassals/test_django.ini
    ```

10. [debugging] gunicorn
    1. make sure socket has active status
    ```
        systemctl status test_django.socket
    ```
    2. make sure serivce has active status
        ```
        systemctl status test_django
        ```
    3. make sure you can hit django using gunicorn
        ```
            sudo -u user curl --unix-socket /run/gunicorn.sock http
        ```
    4. enable service
    ```
        systemctl enable --now test_django.socket
    ```

11. add user to nginx group
    ```
        gpasswd -a django nginx
    ```
11. verify the .sock file
12. install nginx

 1. all server lives inside ```http directive``` in ```nano /etc/nginx/nginx.conf```
 2. create a file inside ```touch /etc/nginx/conf.d/test_project.conf``` All files are automatically imported in nginx.conf
 3. copy the sample
```
   upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8000; # for a web port socket (we'll use this first)
}

server {
    listen 81 ssl;
     listen [::]:81 ssl;
    server_name website_name www.website_name; # Name of server
    ssl_certificate     /etc/ssl/certs/server_name.crt;
    ssl_certificate_key /etc/ssl/certs/server_name.key;
      # rewrite to remove www.
        if ( $host ~ ^www\.(.+)$ ) {
            set $without_www $1;
            rewrite ^ $scheme://$without_www$uri permanent;
        }
    # redirect http to https
    error_page 497 https://$server_name:$server_port$request_uri;

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
            #uwsgi_pass unix:/tmp/uwsgi/test_project.sock;
            #uwsgi_pass  django;
            #include uwsgi_params;
            proxy_pass http://unix:/run/test_django.sock;
        }
}
```

12. copy
```
nginx -t
```
13. run
```
sudo nginx -s reload
```
14. run
```
systemctl status nginx.service
```
15. run
    ```
    netstat -na|grep LISTEN | grep :81
    ```



### Additional information
1. white list IPs
Log into WHM as the 'root' user.
Navigate to "Home / Plugins / ConfigServer Security & Firewall / Firewall Configuration."
Click the "csf" tab.

2. Enable SSL || https
    1. Go to SSL/TLS and create key and crt
    2. save it in /etc/ssl/certs
    3. Go to nginx configuration stated above in ssl_certificate and update it

3. Enable Auto SSL
    1. Go to ```SSL/TLS Status```
    2. choose domain and select ```Run Auto SSL```