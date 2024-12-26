from django.core.management.base import BaseCommand
from apps.users.models import Role, Permission, RoleUser, User
from utils.helpers import create_default_roles_and_permissions, create_default_users

import json

class Command(BaseCommand):
    help = 'Seed the database with default roles, permissions, and users'

    def handle(self, *args, **kwargs):
        create_default_roles_and_permissions()  # Seed roles and permissions
        create_default_users()  # Seed default users
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with roles, permissions, and users!'))
        # Create Roles
        admin_role, created = Role.objects.get_or_create(name='Admin')
        manager_role, created = Role.objects.get_or_create(name='Manager')
        employee_role, created = Role.objects.get_or_create(name='Employee')

        # Define Permissions for each Role (JSON format)
        admin_permissions = {
            'create': True,
            'update': True,
            'delete': True,
            'view': True
        }
        manager_permissions = {
            'create': True,
            'update': True,
            'delete': False,  # Managers cannot delete
            'view': True
        }
        employee_permissions = {
            'create': False,  # Employees cannot create
            'update': False,  # Employees cannot update
            'delete': False,  # Employees cannot delete
            'view': True
        }

        # Assign Permissions to Roles
        Permission.objects.get_or_create(role=admin_role, permission_json=admin_permissions)
        Permission.objects.get_or_create(role=manager_role, permission_json=manager_permissions)
        Permission.objects.get_or_create(role=employee_role, permission_json=employee_permissions)

        # Create Users and Assign Roles
        admin_user = User.objects.create_user(username='admin_user', password='adminpass123')
        manager_user = User.objects.create_user(username='manager_user', password='managerpass123')
        employee_user = User.objects.create_user(username='employee_user', password='employeepass123')

        RoleUser.objects.get_or_create(role=admin_role, user=admin_user)
        RoleUser.objects.get_or_create(role=manager_role, user=manager_user)
        RoleUser.objects.get_or_create(role=employee_role, user=employee_user)

        # Print the result to the console
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with roles, permissions, and users!'))
