from rest_framework import generics, status
from rest_framework.generics import ListAPIView

from rest_framework.response import Response
from .models import Salary
from .serializers import SalarySerializer
from .services import saveSalary, getSalaries
from apps.users.models import User
from rest_framework.views import APIView


class CreateSalaryView(generics.CreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer

    def post(self, request, *args, **kwargs):
        response = saveSalary(self, request, User)
        return response

class GetSalaries(ListAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    