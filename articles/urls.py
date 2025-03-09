from django.urls import path
from .views import ArticlesListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'articles'

urlpatterns = [
    path('', ArticlesListView.as_view(), name='all-articles'),
    path('create-article/', ArticleCreateView.as_view(), name='create-article'),
    path('<slug:slug>', ArticleDetailView.as_view(), name='article'),
    path('edit-article/<slug:slug>', ArticleUpdateView.as_view(), name='edit-article'),
    path('delete-article/<slug:slug>', ArticleDeleteView.as_view(), name='delete-article')
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
