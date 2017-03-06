from django.conf.urls import include, url
from app import views, ajax, class_view

urlpatterns = [
    # Examples:
    # url(r'^$', 'wikibooks.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),

    # BEGIN BOOK
    url(r'^books/(?P<id>\d+)/$', views.book_details, name='book_details'),
    url(r'^books/add/$', views.book_add, name='book_add'),
    url(r'^books/get/(?P<id>\d+)/$', views.book_get, name='book_get'),
    # END BOOK

    # BEGIN AUTHOR
    url(r'^authors/(?P<id>\d+)/$', views.author, name='author'),
    url(r'^authors/$', views.author_list, name='author_list'),
    # url(r'^author/(?P<id>.+)/$', views.author_name, name='author_name'),
    # END AUTHOR

    # BEGIN TAG
    url(r'^tags/(?P<id>.+)/$', views.tag, name='tag'),
    url(r'^tags/$', views.tag_list, name='tag_list'),
    # END TAG
    
 	# BEGIN COMMENT
    url(r'^comment/$', views.comment, name='comment'),
    # END COMMENT
    
    # BEGIN SEARCH
    url(r'^search/$', views.search, name='search'),
    # END SEARCH

    # BEGIN USER
    url(r'^users/(?P<id>\d+)/$', views.user, name='user'),
    # url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/login/$', views.user_login, name='user_login'),
    url(r'^users/logout/$', views.user_logout, name='user_logout'),
    url(r'^users/register/$', views.user_register, name='user_register'),
    url(r'^users/activate/(?P<token_str>.+)$', views.user_activate, name='user_activate'),
    # END USER
    
    # BEGIN AJAX
    url(r'^ajax/get_tags/$', ajax.get_tags, name='ajax_get_tags'),
    url(r'^ajax/get_authors/$', ajax.get_authors, name='ajax_get_authors'),
    # END AJAX
    
    url(r'^hello/$', class_view.HelloView.as_view(), name='hello'),
]
