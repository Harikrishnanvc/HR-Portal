from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from chat.api import MessageModelViewSet, UserModelViewSet

import notifications.urls
#
router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path(r'', TemplateView.as_view(template_name='chat/chat.html'), name='employee_chat'),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
