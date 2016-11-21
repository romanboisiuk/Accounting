from django.conf.urls import  url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from views import journal, groups, contact_admin, students
from views.students import StudentUpdateView, StudentDeleteView, StudentAddView
from views.groups import GroupDeleteView, GroupUpdateView, GroupAddView
from views.journal import JournalView
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [ 
	# Students urls
    url(r'^$', students.students_list, name='home'),
    url(r'^students/add/$', StudentAddView.as_view(), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

  # Groups urls
    url(r'^groups/$', groups.groups_list, name='groups'),
    url(r'^groups/add/$', GroupAddView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),
    
    # Journal  urls
  	url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

     # Contact Admin Form
    url(r'^contact_admin/$', contact_admin.contact_admin, name='contact_admin'),

    # Users urls
    #url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, 
     # name='auth_logout'),
    #url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), 
     # name='registration_complete'),

    url(r'^users/', include('registration.backends.simple.urls')),
]

