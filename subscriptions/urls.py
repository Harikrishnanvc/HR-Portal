from django.urls import path
from subscriptions import views
from subscriptions.views import InitiatePaymentAPI
urlpatterns = [
    path('subscription/', views.home, name='subscriptions-home'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session, name='check-out'),
    path('success/', views.success),
    path('cancel/', views.cancel),
    path('webhook/', views.stripe_webhook, name='webhook'),
    path('initiate-payment-api/', InitiatePaymentAPI.as_view() , name='initiate-payment'),
    ]