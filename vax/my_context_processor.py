from datetime import datetime
from vax.models import User

def date_and_version(request):
    ctx = {
    "now": datetime.now(),
    "version": "0.0",
    }
    return ctx

def current_user(request, user_id):
    user = User.objects.get(id=user_id)
    ctx = {
        "user": user.username
    }