from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Cprices.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'accounts.views.home'),
    url(r'^login/$', 'accounts.views.login'),
    url(r'^logout/$', 'accounts.views.logout'),
    url(r'^register/$', 'accounts.views.register'),
    url(r'^forgotpasswd/$', 'accounts.views.forgotpasswd'),
    url(r'^changepasswd/$', 'accounts.views.changepasswd'),
    url(r'lists/$', 'crawler.views.lists'),
    url(r'realupdate/$', 'crawler.views.realupdate'),
    url(r'detail/(?P<item_id>\d+)', 'crawler.views.detail'),
    url(r'track/$', 'crawler.views.track'),
    url(r'detrack/(?P<item_id>\d+)', 'crawler.views.detrack'),
    url(r'search/$', 'crawler.views.search'),
)
