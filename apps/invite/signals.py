from django.core.mail import send_mail


def send_invitation(sender, created, instance=None, **kwargs):
    if not created:
        # we only want to send an email when the invitation is first created
        return
    send_mail(
        # Subject
        'Invitation to join {0}'.format(instance.trip.title),
        # Message
        'Hey there!\n\n'
        'You have been invited to join {0} on TripHub!\n'
        'Head to https://triphub-app.herokuapp.com/i/{1} to join.\n\n'
        'Happy tripping 🌍'
        .format(instance.trip.title, instance.uid),
        # From
        'from@triphub.com',
        # To
        [instance.email],
        fail_silently=False,
    )
