from admin_panel.models import *


def getBanner():
    return BackImg.objects.first()

def baseView(request):
    return {
        'banner': getBanner(),
        'pages': Page.objects.all()
    }