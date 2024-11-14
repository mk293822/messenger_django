from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class User_Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images', default='avatar.svg')
    friends = models.ManyToManyField(User, related_name='friends', blank=True, null=True)
    request_friend = models.ManyToManyField(User, related_name='friend_request', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def fri_check(self):
        """Ensure the user cannot be their own friend."""
        if self.user in self.friends.all():
            raise ValidationError(f"{self.user.username} cannot be friends with themselves.")

    def clean(self):
        """Override the clean method to include custom validation."""
        self.fri_check()
        # Additional validations can go here

    def save(self, *args, **kwargs):
        """Override save to ensure custom validations are applied."""
        self.full_clean()  # This will call the clean method
        super().save(*args, **kwargs)


# Private Room model for one-to-one chats between two users
class Private_rooms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    created = models.DateTimeField(auto_now=True, editable=False)
    updated = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return str(self.id)


# Private Messages model for messages in a private room
class Private_messages(models.Model):
    room = models.ForeignKey(Private_rooms, on_delete=models.CASCADE, related_name='private_messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_messages')  
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.content[0:50] 


#  Group chat model for rooms that multiple users can join
class Rooms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_rooms')  
    participants = models.ManyToManyField(User, related_name='joined_rooms') 
    created = models.DateTimeField(auto_now=True, editable=False)
    updated = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return str(self.id)



#  Messages model for group chat
class Messages(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_messages')  
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content[0:50] 
