from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test


class GroupRequiredMixin(UserPassesTestMixin):
    """Mixin that requires user to belong to specific group(s)."""
    required_groups = []

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        user_groups = set(self.request.user.groups.values_list('name', flat=True))
        return bool(user_groups.intersection(set(self.required_groups)))


class RoleRequiredMixin(UserPassesTestMixin):
    """Mixin that requires user to have a specific role."""
    allowed_roles = []

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        if hasattr(user, 'profile'):
            return user.profile.role in self.allowed_roles
        return False


def role_required(allowed_roles):
    """Decorator for views that checks that the user has a specific role."""
    def check_role(user):
        if user.is_superuser:
            return True
        if hasattr(user, 'profile'):
            return user.profile.role in allowed_roles
        return False
    return user_passes_test(check_role)

import csv
from django.http import HttpResponse

class CSVExportMixin:
    """Mixin to add CSV export capabilities to a Django ListView."""
    csv_filename = 'export.csv'
    csv_export_fields = None  # List of tuples: [('Field Header', 'model_field_or_property')]

    def get(self, request, *args, **kwargs):
        if 'export' in request.GET and request.GET['export'] == 'csv':
            queryset = self.get_queryset()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{self.csv_filename}"'
            
            writer = csv.writer(response)
            
            if self.csv_export_fields:
                # Write headers
                headers = [header for header, field in self.csv_export_fields]
                writer.writerow(headers)
                
                # Write data
                for obj in queryset:
                    row = []
                    for header, field in self.csv_export_fields:
                        # Handle nested fields like 'vehicle.registration_number'
                        if '.' in field:
                            parts = field.split('.')
                            val = obj
                            for part in parts:
                                val = getattr(val, part, '') if val else ''
                        else:
                            val = getattr(obj, field, '')
                            
                        # Resolve callables (e.g. get_status_display)
                        if callable(val):
                            val = val()
                        row.append(str(val) if val is not None else '')
                    writer.writerow(row)
            else:
                # Fallback to all fields if none specified
                fields = [f.name for f in queryset.model._meta.fields]
                writer.writerow(fields)
                for obj in queryset:
                    row = [str(getattr(obj, field, '')) for field in fields]
                    writer.writerow(row)
                    
            return response
            
        return super().get(request, *args, **kwargs)
