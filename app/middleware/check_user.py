from django.contrib.auth.models import User
from app.models import *

class CheckUser(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if request.user.is_authenticated and request.user.lastPull.waitingMerge:
        #     raise Exception('Your last pull request is waiting for a merge. Please try again later.')
        users = list(User.objects.all())
        if not users:
            user = User.objects.create_user(
                username='admin',
                first_name='admin',
                last_name='admin',
                password='admin',
                is_superuser= True,
                email=''
            )
            for perm in request.POST.getlist('permissions'):
                permission, created= Permissions.objects.get_or_create(permissionsCollege=perm)
                user.permissions.add(permission.id)
            LastPull.objects.create(userId= user)
            UserSynchronization.objects.create(userId= user)
        response = self.get_response(request)

        return response

    
   