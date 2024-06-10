from django import template

register = template.Library()

@register.filter
def get_profile(profiles_dict, user):
    if isinstance(profiles_dict, dict):
        return profiles_dict.get(user)
    else:
        # Handle the case where profiles_dict is not a dictionary
        return None  # Or any other appropriate value
