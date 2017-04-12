from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pre_process$', views.pre_process_text, name='pre_process'),
    url(r'^lines/(?P<line_num>\d+)/$', views.get_line, name='get_line'),
]