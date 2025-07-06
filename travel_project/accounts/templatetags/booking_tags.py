from django import template

register = template.Library()

@register.filter
def status_color(status):
    color_map = {
        'pending': 'warning',
        'confirmed': 'success',
        'rejected': 'danger',
        'cancelled': 'secondary'
    }
    return color_map.get(status.lower(), 'primary')

@register.filter
def payment_status_color(status):
    color_map = {
        'pending': 'warning',
        'completed': 'success',
        'refunded': 'info',
        'failed': 'danger'
    }
    return color_map.get(status.lower(), 'primary') 