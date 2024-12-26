from apps.users.models import Role, Permission, RoleUser, User
import json
from rest_framework_simplejwt.tokens import AccessToken

def create_role(name):
    """
    Create a role in the database if it does not already exist.
    """
    role, created = Role.objects.get_or_create(name=name)
    return role

def create_permission(role, permission_json):
    """
    Create permissions for a given role. Permissions are stored as JSON.
    """
    permission, created = Permission.objects.get_or_create(role=role, permission_json=permission_json)
    return permission

def create_user(username, password):
    """
    Create a user and hash their password automatically.
    """
    user = User.objects.create_user(username=username, password=password)
    return user

def assign_role_to_user(user, role):
    """
    Assign a role to a user.
    """
    role_user, created = RoleUser.objects.get_or_create(role=role, user=user)
    return role_user

def create_default_roles_and_permissions():
    """
    Create default roles and permissions for the application.
    """
    # Create roles
    admin_role = create_role('Admin')
    manager_role = create_role('Manager')
    employee_role = create_role('Employee')

    # Create permissions for Admin role
    admin_permissions = {
        'create': True,
        'update': True,
        'delete': True,
        'view': True
    }
    create_permission(admin_role, admin_permissions)

    # Create permissions for Manager role
    manager_permissions = {
        'create': True,
        'update': True,
        'delete': False,  # Managers cannot delete
        'view': True
    }
    create_permission(manager_role, manager_permissions)

    # Create permissions for Employee role
    employee_permissions = {
        'create': False,  # Employees cannot create
        'update': False,  # Employees cannot update
        'delete': False,  # Employees cannot delete
        'view': True
    }
    create_permission(employee_role, employee_permissions)

def create_default_users():
    """
    Create default users and assign roles to them.
    """
    # Create default users
    admin_user = create_user('admin_user', 'adminpass123')
    manager_user = create_user('manager_user', 'managerpass123')
    employee_user = create_user('employee_user', 'employeepass123')

    # Assign roles to users
    admin_role = Role.objects.get(name='Admin')
    manager_role = Role.objects.get(name='Manager')
    employee_role = Role.objects.get(name='Employee')

    assign_role_to_user(admin_user, admin_role)
    assign_role_to_user(manager_user, manager_role)
    assign_role_to_user(employee_user, employee_role)

def check_user_permission(user, action):
    """
    Check if a user has permission to perform a specific action.
    """
    # Get all roles for the user
    role_users = RoleUser.objects.filter(user=user)

    for role_user in role_users:
        role = role_user.role
        # Get the permissions for the role
        permissions = Permission.objects.filter(role=role)
        
        for permission in permissions:
            # Check if the action is allowed for this role
            if permission.permission_json.get(action):
                return True  # The user has permission for this action
    
    return False  # The user does not have permission for the action




def generate_non_expiring_token(user):
    """
    Generate a JWT token that never expires for a given user.
    """
    token = AccessToken.for_user(user)
    # Remove the 'exp' claim to make it non-expiring
    del token['exp']
    return str(token)