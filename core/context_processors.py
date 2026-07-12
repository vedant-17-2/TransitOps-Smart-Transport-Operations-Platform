from fleet.models import Vehicle
from drivers.models import Driver
from trips.models import Trip


def global_context(request):
    """Add global context variables available to all templates."""
    context = {
        'app_name': 'TransitOps',
        'app_tagline': 'Smart Transport Operations Platform',
    }
    if request.user.is_authenticated:
        role = None
        if hasattr(request.user, 'profile'):
            role = request.user.profile.role

        all_nav_items = [
            {'name': 'Dashboard', 'url': '/', 'icon': 'bi-speedometer2', 'id': 'dashboard', 'roles': ['all']},
            {'name': 'Vehicles', 'url': '/fleet/', 'icon': 'bi-truck', 'id': 'fleet', 'roles': ['fleet_manager', 'dispatcher']},
            {'name': 'Drivers', 'url': '/drivers/', 'icon': 'bi-person-badge', 'id': 'drivers', 'roles': ['fleet_manager', 'dispatcher', 'safety_officer']},
            {'name': 'Trips', 'url': '/trips/', 'icon': 'bi-signpost-2', 'id': 'trips', 'roles': ['dispatcher', 'fleet_manager']},
            {'name': 'Maintenance', 'url': '/maintenance/', 'icon': 'bi-wrench-adjustable', 'id': 'maintenance', 'roles': ['fleet_manager', 'financial_analyst']},
            {'name': 'Fuel & Expenses', 'url': '/fuel/', 'icon': 'bi-fuel-pump', 'id': 'fuel', 'roles': ['fleet_manager', 'financial_analyst']},
            {'name': 'Analytics', 'url': '/analytics/', 'icon': 'bi-graph-up', 'id': 'analytics', 'roles': ['fleet_manager', 'financial_analyst']},
        ]

        # Filter based on role
        if request.user.is_superuser:
            nav_items = all_nav_items
        else:
            nav_items = [item for item in all_nav_items if 'all' in item['roles'] or role in item['roles']]

        context.update({'nav_items': nav_items})
    return context
