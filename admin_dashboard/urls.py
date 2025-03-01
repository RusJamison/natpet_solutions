from django.urls import path

from admin_dashboard import views 

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='admin_index'),
    path('products/', views.AdminProductListView .as_view(), name='admin_product_list'),
    path('product/<int:pk>/', views.AdminProductDetailView.as_view(), name='admin_product_detail'),
    path('products/<int:pk>/delete/', views.AdminProductDeleteView.as_view(), name='admin_product_delete'),
    path('categories/', views.AdminCategoryListView.as_view(), name='admin_category_list'),
    path('category/<int:pk>/', views.AdminCategoryDetailView.as_view(), name='admin_category_detail'),
    path('category/<int:pk>/delete/', views.AdminCategoryDeleteView.as_view(), name='admin_category_delete'),
    path('manufacturers/', views.AdminManufacturerListView.as_view(), name='admin_manufacturer_list'),
    path('maunufacturer/<int:pk>/', views.AdminManufacturerDetailView.as_view(), name='admin_manufacturer_detail'),
    path('maunufacturer/<int:pk>/delete/', views.AdminManufacturerDeleteView.as_view(), name='admin_manufacturer_delete'),
    path('orders/', views.AdminOrderListView.as_view(), name='admin_order_list'),
    path('orders/<int:pk>/', views.AdminOrderDetailView.as_view(), name='admin_order_detail'),
    path('orders/<int:pk>/delete/', views.AdminOrderDeleteView.as_view(), name='admin_order_delete'),
    path('coupons/', views.AdminCouponListView.as_view(), name='admin_coupon_list'),
    path('coupon/<int:pk>/', views.AdminCouponDetailView.as_view(), name='admin_coupon_detail'),
    path('coupon/<int:pk>/delete/', views.AdminCouponDeleteView.as_view(), name='admin_coupon_delete'),
]
