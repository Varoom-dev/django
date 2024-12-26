from django.urls import path
from .views import CreateSalaryView, GetSalaries

urlpatterns = [
    path('salary/create/', CreateSalaryView.as_view(), name='create_salary'),
    path('salary/', GetSalaries.as_view(), name='get_salary'),

]