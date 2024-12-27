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
