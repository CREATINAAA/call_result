from django.urls import path

from .views import LeadTransferAPIView, LeadCreationAPIView, UnqualifiedLeadCreationAPIView

urlpatterns = [
    path('lead-moloko/', LeadCreationAPIView.as_view(), name='lead-moloko'),
    path('lead-moloko-unqualified/', UnqualifiedLeadCreationAPIView.as_view(), name='lead-moloko-unqualified'),
    path('lead-transfer/', LeadTransferAPIView.as_view(), name='lead_transfer'),
]
