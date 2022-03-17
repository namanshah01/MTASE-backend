from django.urls import path
from .views import TestView, SummariseAnalyseView

urlpatterns = [

    path('summarise', SummariseAnalyseView.as_view(), name="summarise"),
    path('test', TestView.as_view(), name="test"),

]