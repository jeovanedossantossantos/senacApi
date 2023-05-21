from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TarefaViews




urlpatterns = [
    path('', TarefaViews.as_view(), name='tarefa-list'),
    path('<id>/', TarefaViews.as_view(), name='tarefa-detail'),
    
    
]
urlpatterns = format_suffix_patterns(urlpatterns)