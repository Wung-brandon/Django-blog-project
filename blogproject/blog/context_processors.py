from .models import UserProfile

def user_profile(request):
    
    if request.user.is_authenticated:
        try:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None
    else:
        user_profile = None

    return {'user_profile': user_profile}
