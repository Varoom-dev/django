from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator

def saveSalary(self, request, User):
    user_id = request.data.get('user_id')
    amount = request.data.get('amount')
    
    # Validate employee existence
    try:
        user_id = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize and save salary data
    serializer = self.get_serializer(data={"employee_id": user_id.id, "amount": amount})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

def getSalaries(self, request, User):
    salaries = Salary.objects