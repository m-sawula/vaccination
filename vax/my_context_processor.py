from datetime import datetime
from django.contrib.auth.models import User

def date_and_version(request):
    ctx = {
    "now": datetime.now(),
    "version": "0.0",
    }
    return ctx

def current_user(request):
    user = request.user
    if request.user.is_authenticated:
        return {"user": user}

