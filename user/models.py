from django.db import models
from django.contrib.auth.models import User
from lawyer.models import Lawyer_Profile
from django.db.models import Max
from django.forms import DateTimeField
from django.contrib.auth import get_user_model
from django.db.models import Q


# Create your models here.


class Complete_Profile(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to="profile/")
    address=models.TextField()
    city=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    zip=models.IntegerField()
    mobile=models.IntegerField()




class Contact_lawyer(models.Model):
    lawyer=models.ForeignKey(Lawyer_Profile,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user")
    matter=models.CharField(max_length=255)
    complaint=models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    reciepient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def sender_message(from_user, to_user, body):
        sender_message = Contact_lawyer(
            user=from_user,
            sender=from_user,
            reciepient=to_user,
            body=body,
            is_read=True
        )
        sender_message.save()

        reciepient_message = Contact_lawyer(
            user=to_user,
            sender=from_user,
            reciepient=from_user,
            body=body,
            is_read=True
        )
        reciepient_message.save()
        return sender_message

    def get_message(user):
        users = []
        messages = Contact_lawyer.objects.filter(user=user).values('reciepient').annotate(last=Max('date')).order_by(
            '-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['reciepient']),
                'last': message['last'],
                'unread': Contact_lawyer.objects.filter(user=user, reciepient__pk=message['reciepient'],
                                                 is_read=False).count()
            })
        return users
class Message(models.Model):
    from_user = models.ForeignKey(Lawyer_Profile, related_name='messages', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,  related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

