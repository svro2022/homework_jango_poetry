from django.urls import path

from .apps import CatalogConfig
from .views import MainListView, ProductsListView, CategoriesListView, CategoryProductsListView, ProductDetailView
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    # CATALOG
    #FBV path('', index, name='index'),
    path('', MainListView.as_view(), name='index'),
    #FBV path('categories/', categories, name='categories'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    #FBV path('<int:pk>/products/', category_products, name='category_products'),
    path('<int:pk>/products/', CategoryProductsListView.as_view(), name='category_products'),
    #FBV path('productsall/', products, name='products'),
    path('productsall/', ProductsListView.as_view(), name='products'),
    #FBV path('<int:pk>/product/', product_detailed, name='product_detailed'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product_detailed'),
    # BLOG
    path('blog/', BlogListView.as_view(), name='blog_index'),
    path('<int:pk>/blog/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('<int:pk>/blog/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/blog/delete/', BlogDeleteView.as_view(), name='blog_delete'),

]
