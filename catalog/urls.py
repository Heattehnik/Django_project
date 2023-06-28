from django.urls import path
from catalog.views import contacts, ProductDetailView, ProductListView, ArticleListView, ArticleCreateView, \
    ArticleDetailedView, ArticleUpdateView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='catalog'),
    path('contacts/', contacts, name='contacts'),
    path('product_card/<int:pk>/', ProductDetailView.as_view(), name='product_card'),
    path('blog/', ArticleListView.as_view(), name='articles'),
    path('blog/create/', ArticleCreateView.as_view(), name='create_article'),
    path('blog/view/<int:pk>/', ArticleDetailedView.as_view(), name='view_article'),
    path('blog/edit/<int:pk>/', ArticleUpdateView.as_view(), name='edit_article')
]
