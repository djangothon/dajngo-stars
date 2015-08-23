from django.conf.urls import url
from . import ajax_views

urlpatterns = [
    url(r'^show-rating/(?P<ctype_id>\d+)/(?P<object_id>\d+)$',
        'stars.ajax_views.show_rating',
        name='show_rating'),

    url(r'^get-rating/(?P<ctype_id>\d+)/(?P<object_id>\d+)/(?P<decoration>\d+)/$',
        'stars.ajax_views.get_rating',
        name='get_rating'),

    url(r'^submit-user-rating/(?P<ctype_id>\d+)/(?P<object_id>\d+)/(?P<decoration>\d+)/$',
        'stars.ajax_views.submit_user_rating',
        name='submit_user_rating'),

    url(r'^clear-user-rating/(?P<ctype_id>\d+)/(?P<object_id>\d+)/(?P<decoration>\d+)/$',
        'stars.ajax_views.clear_user_rating',
        name='clear_user_rating'),
]