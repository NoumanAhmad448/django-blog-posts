from django.db import migrations
from api_v1.models.create_post_model import CreatePostModel
from django.contrib.sites.models import Site
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
                ('auths', '0002_alter_passwordhistory_options_and_more'),
    ]
    def add_site_key(apps, schema_editor):
        CreatePostModel = apps.get_model("api_v1", "CreatePostModel")
        posts = CreatePostModel.objects.all()

        app_id=settings.SITE_ID

        if posts is not None:
            for post in posts:
                site = Site.objects.filter(id=app_id).first().id
                post.site.add(site)

    operations = [
        migrations.RunPython(add_site_key)
    ]

