from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TravelStyle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserTravelStyle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="travel_style_pref")
    travel_style = models.ForeignKey(TravelStyle, on_delete=models.SET_NULL, null=True, related_name="users")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.travel_style.name if self.travel_style else 'No Style'}"
