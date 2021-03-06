from django.urls import path
from taxmust import views


urlpatterns = [
    path('', views.index, name='index_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('add-service/<int:customer_id>/',
         views.select_service, name='select_service'),
    path('update-documents/<int:customer_id>/<int:service_id>/',
         views.update_documents, name='update_documents'),
    # path('/taxmust/payment/<int:order_id>/', views.payment, name='payment')
    path('view-orders/', views.view_orders, name="view_orders"),
    path('order/<int:id>/', views.order_details, name="view_orders"),
    path('checkout/<int:order_id>', views.checkout, name="checkout"),
    path('payment-success-url/<int:order_id>/', views.payment_success_url, name="payment_success_url"),
    path('administration/', views.administration, name='adminsitration'),
    path('view-all-orders/', views.view_all_orders, name='view_all_orders'),
    path('order-details/<int:id>/', views.admin_orders, name="admin_orders"),
    path('update-status/<int:id>/', views.update_status, name="update_status"),
    path('add-note/<int:id>/', views.add_note, name="add_note")
]
