from django.conf.urls.defaults import *
from tod.prompt.models import Prompt
urlpatterns = patterns('tod.prompt.views', 
    (r'^(?P<prompt_id>\d+)/complete/$', 'complete'),
    (r'^create/$', 'detail'),
    (r'^$', 'limited_object_list',  {'queryset': Prompt.objects.all(),}),
    (r'^(?P<object_id>\d+)/delete/$', 'limited_delete_object', {'model': Prompt, 'post_delete_redirect': '/prompt/'}),
)

