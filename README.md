# Blog Posts Project
### An app that can create blogs. The main purpose to create this app to practice django skills and make the source code available online for other developers to start this repo for their own custom need
Using this app, you can
1. create an account, update the user password, login to the website
2. fetch the user detail using API
3. create a token for API validation
4. localization has been implementated for english and chinese languages. You can pass a get params lang=en|zh

![Alt home page](md_images/01.png "Home Page")
![Alt reg page](md_images/02.png "Registeration Page")
![Alt login page](md_images/03.png "Login Page | in chinese")
![Alt create a post](md_images/04.png "Create a Post")
![Alt list page](md_images/05.png "List the Post")

## Setup (Recommended)
1. install anaconda
2. create an environment using
``` conda create -n "django-blog-posts" python=3.10```
3. run ```conda activate django-blog-posts```
4. run ```pip install -r requirements.txt```
5. replace file name in blog_posts/copy_settings.py to settings.py
5. you need to setup database(mysql) in ```settings.py```
6. create a database ```django_blog_posts``` in the database
7. run migrations using ```python manage.py migrate```
8. run ```python manage.py runserver```

# Auto Deployment using Github Actions
1. you may refer to deployment.yml file in github Action for deployment

# Dockering Version
1. run command ```docker-compose up```

## locationlization rules
1. install gettext. follow django documentation or Google it
2. following commands can be handy while creating locationlization
    1. django-admin makemessages --locale=zh --extension=html,txt,py
    2. django-admin compilemessages

## Information
1. super user credentials: username: test_user  password:Silver009@t

## Technical Knowledge
1. custom middleware has been created for language translation ```middlewares.LanguageTransMiddleware```
2. django session and token validation has been implemented
3. front end has been developed using Jquery & Bootstrap
4. ```Postman collection has been made online for public use```
5. django custom template tags and filter
6. Serializer, form validation have been implemented