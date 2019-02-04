from django.conf.urls import url

from oscarapi.app import RESTApiApplication

from . import views


class MyRESTApiApplication(RESTApiApplication):

    def get_urls(self):
        urls = [url(
            r'^products/$',
            views.ProductList.as_view(), name='product-list'),
            url(
            r'^categories/$',
            views.CategoryList.as_view(), name='categories'),
            url(r'^categories/(?P<pk>[0-9]+)/$',
            views.CategoryDetail.as_view(), name='category-detail')
        ]

        return urls + super(MyRESTApiApplication, self).get_urls()


application = MyRESTApiApplication()
