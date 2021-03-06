from django.contrib.auth.models import User
from django.db import models
from django_unixdatetimefield import UnixDateTimeField


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    private_key = models.TextField(max_length=8192)
    public_key = models.TextField(max_length=8192)
    mobile_number = models.CharField(max_length=15, blank=True)
    two_factor = models.BooleanField(default=False)
    theme = models.IntegerField(default=0)
    online_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class ContactRequest(models.Model):
    requestee = models.ForeignKey(UserProfile, related_name='requestee')
    requested = models.ForeignKey(UserProfile, related_name='requested')
    accepted = models.BooleanField(default=False)

class Contact(models.Model):
    contact1 = models.ForeignKey(UserProfile, related_name='contact1')
    contact2 = models.ForeignKey(UserProfile, related_name='contact2')

class Chat(models.Model):
    participants = models.ManyToManyField(UserProfile)

class Message(models.Model):
    content_type = models.TextField(max_length=8192)
    content = models.TextField(max_length=8192)
    time_sent = UnixDateTimeField()
    sender = models.ForeignKey(UserProfile)
    chat = models.ForeignKey(Chat)

class ContactUsForm(models.Model):
    message = models.TextField(max_length=4096)
    email = models.EmailField(blank=True, null=True)
