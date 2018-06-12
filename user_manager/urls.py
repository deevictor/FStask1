from django.conf.urls import url
from . import views as my_views
from django.contrib.auth import views as auth_views

# app_name = 'user_manager'

urlpatterns = [
    url(r'^$', my_views.home, name='home'),
    # url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^login/$', my_views.login_user, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^signup/$', my_views.signup, name='signup'),
    url(r'^contact/$', my_views.contact, name='contact'),
    url(r'^contact_admins/$', my_views.contact_admins, name='contact_admins')
]
