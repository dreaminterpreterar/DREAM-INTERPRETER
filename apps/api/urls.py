from django.urls import path
from .views import CreateInterpretationView, GetInterpretationsView

app_name = 'api'

urlpatterns = [
    path('interpretations/<str:user>/', GetInterpretationsView.as_view()),
    path('create/', CreateInterpretationView.as_view()),
]