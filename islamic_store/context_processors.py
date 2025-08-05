from accounts.models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'notif_count': count}
    return {'notif_count': 0}
