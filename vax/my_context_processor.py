from datetime import datetime

def date_and_version(request):
    ctx = {
    "now": datetime.now(),
    "version": "0.0",
    }
    return ctx