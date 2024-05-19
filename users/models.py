from django.db import models
from aiogram.types import Message
from asgiref.sync import sync_to_async

from utils.info import extract_user_data_from_update


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    user_id = models.PositiveBigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", null=True, blank=True)
    deep_link = models.CharField(max_length=64, null=True, blank=True)
    is_blocked_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"@{self.username}" if self.username else f"{self.user_id}"

    @classmethod
    async def get_user_and_created(cls, message: Message):
        """Get or create a User instance from a Message."""
        data = extract_user_data_from_update(message)
        user, created = await sync_to_async(cls.objects.update_or_create)(
            user_id=data["user_id"], defaults=data
        )
        return user, created

    @classmethod
    async def get_user(cls, message: Message):
        """Retrieve a User instance, creating it if necessary."""
        user, _ = await cls.get_user_and_created(message)
        return user

    @classmethod
    async def get_user_by_username_or_user_id(cls, username_or_user_id):
        """Search for a user in the database by username or user_id."""
        identifier = str(username_or_user_id).replace("@", "").strip().lower()
        if identifier.isdigit():  # user_id
            return await sync_to_async(cls.objects.filter(user_id=int(identifier)).first)()
        return await sync_to_async(cls.objects.filter(username__iexact=identifier).first)()

    @property
    def invited_users(self):
        """Return users who were invited by this user."""
        return User.objects.filter(
            deep_link=str(self.user_id), created_at__gt=self.created_at
        )

    @property
    def tg_str(self) -> str:
        """Return a string representation of the user for Telegram."""
        if self.username:
            return f"@{self.username}"
        return f"{self.first_name} {self.last_name}".strip()
    

