from django.urls import path
from .views import TestView, SummariseAnalyseView, ExtractiveSummaryView

urlpatterns = [

    path('summarise', SummariseAnalyseView.as_view(), name="summarise"),
    path('extractive', ExtractiveSummaryView.as_view(), name="extractive"),
    path('test', TestView.as_view(), name="test"),

]
