from api_v1.models.create_post_model import BlogSitemap
from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.flatpages.sitemaps import FlatPageSitemap

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ["register_user","login_user","logout","blog:bookmark_post",
                "blog:unbookmark_post"]

    def location(self, item):
        return reverse(item)


sitemaps ={
    "blog": BlogSitemap(),
    "flatpages": FlatPageSitemap,
    "static": StaticViewSitemap
}