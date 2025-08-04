from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TravelStyle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Destination(models.Model):

    name = models.CharField(max_length=255)
    province = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    proximate_nature = models.FloatField()
    thrill_activities = models.FloatField()
    cultural_sites = models.FloatField()
    spa_facilities = models.FloatField()

    travel_styles = models.ManyToManyField(TravelStyle, related_name='destinations')
    
    def __str__(self):
        self.name



class StyleParameter(models.Model):
    style = models.ForeignKey(TravelStyle, related_name='parameters', on_delete=models.CASCADE)
    key = models.CharField(max_length=100, help_text="مثلاّ 'nature', 'thrill', 'budget'")
    weight = models.FloatField(help_text='وزن پارامتر در امتیازدهی')

    class Meta:
        unique_together = ('style', 'key')
        
    def __str__(self):
        return f"{self.style.name} - {self.key}: {self.weight}"
    
class UserTravelStyle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="travel_style")
    travel_style = models.ManyToManyField(TravelStyle, related_name="users")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s styles"
