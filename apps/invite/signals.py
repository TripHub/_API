from django.core.mail import send_mail


def send_invitation(sender, instance=None, **kwargs):
    send_mail(
        # Subject
        'Invitation to join {0}'.format(instance.trip.title),
        # Message
        'Hey there!\n\n'
        'You have been invited to join {0} on TripHub!\n'
        'Head over to https://triphub-app.herokuapp.com/invite/{1} to join.'
        .format(instance.trip.title, instance.uid),
        # From
        'from@triphub.com',
        # To
        [instance.email],
        fail_silently=False,
    )
