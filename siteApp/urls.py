from django.conf.urls import url
from django.contrib.auth import views as auth_views
from utils import PeriodicThread, CompanyUtils

from .models import Company
from .import views

urlpatterns = [
    url(r'^get_companies_codes/?$', views.get_companies_codes),
    url(r'^get_companies_wikis/?$', views.get_companies_wikis),
    url(r'^include_news/$', views.include_news),
    url(r'^include_company/$', views.include_company),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout,   {'next_page': '/'}),
    url(r'^company/(?P<company_id>[0-9]+)/$', views.company_details, name='company_details'),
    url(r'^register/$', views.register),
    url(r'^follow_company/(?P<company_id>[0-9]+)/?$', views.follow_company),
    url(r'^unfollow_company/(?P<company_id>[0-9]+)/?$', views.unfollow_company),
    url(r'^password_reset/$', auth_views.password_reset, {"template_name":"registration/password_reset_form.html"}),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^$', views.dashboard),
]

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

# RUN SCRAPERS, RUN

from scrapyd_api import ScrapydAPI
from .models import Company

def share_loop():
    for company in Company.objects.all():
        CompanyUtils.updateShares(company)
        company.save()

def stock_loop():
    for company in Company.objects.all():
        company.stock = CompanyUtils.getActualStock([company.nasdaq]);
        company.save()

stock_thread = PeriodicThread(callback=stock_loop, period=(60))
stock_thread.start()

share_thread = PeriodicThread(callback=share_loop, period=(12 * 60 * 60))
share_thread.start()
share_loop()
