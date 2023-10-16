## local development commands
1. Run
```
b:
cd B:\django-blog-posts\blog_posts\frontend-react
npm run dev
```


## Local setup
1. commands
```
npm install
```


## deployment
```
npm install pm2 -g
```
```
pm2 list
```
run next service in the background
```
pm2 start "npm start" -n nextjs.lyskills.com
```
```
pm2 stop     <app_name|namespace|id|'all'|json_conf>
pm2 delete   <app_name|namespace|id|'all'|json_conf>
```
pm2 logs
```
pm2 logs -n nextjs.lyskills.com
```
