import json
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_cryptography.fields import encrypt


class CustomUser(AbstractUser):

    number = models.CharField(max_length=20)
    api_id = models.CharField(max_length=10)
    api_hash = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Groups(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user_groups'
    )
    chats = models.JSONField(
        default=list,
        verbose_name='url of chats'
    )

    def __str__(self):
        return f"{self.user.username} - {self.chats}"

    def add_chats(self, new_links):
        current_chats = self.get_chats()
        added = 0

        for link in new_links:
            if link not in current_chats:
                current_chats.append(link)
                added += 1

        if added > 0:
            self.chats = current_chats
            self.save()
        return added

    def get_chats(self):
        if isinstance(self.chats, str):
            return json.loads(self.chats)
        return self.chats or []


class TelegramSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='telegram_sessions')
    api_id = encrypt(models.CharField(max_length=50))
    api_hash = encrypt(models.CharField(max_length=100))
    phone_number = encrypt(models.CharField(max_length=20))
    session_file = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Telegram Session"