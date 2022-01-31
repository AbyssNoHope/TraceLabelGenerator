from django.urls import path
from .views import SpanView, TraceView

urlpatterns = [
    # post
    path('span/', SpanView.as_view()),
    # get & detele
    path('span/<int:trace_id>/', SpanView.as_view()),
    # post
    path('label/', TraceView.as_view()),
    # get
    path('trace/<int:is_all>', TraceView.as_view()),  # 0 = False, 1=True
]
