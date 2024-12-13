from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from notifications.models import Notification

@api_view(['GET'])
def get_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')

    # Return notifications, filtering unread ones
    unread_notifications = notifications.filter(is_read=False)
    
    # Mark notifications as read
    for notification in unread_notifications:
        notification.is_read = True
        notification.save()

    # You can also include other info like the post or comment in the response
    data = [{"actor": n.actor.username, "verb": n.verb, "target": str(n.target), "timestamp": n.timestamp} for n in notifications]

    return Response(data)




