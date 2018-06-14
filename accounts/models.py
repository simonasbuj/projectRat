from django.db import models

#datetime
from datetime import datetime
from django.utils import timezone
to_tz = timezone.get_default_timezone()
from dateutil import relativedelta

#foreignkeys
from django.contrib.auth.models import User
from library.models import Book

from .helper import user_avatar_upload

# Create your models here.


class Info(models.Model):
    LYTYS = (
        ('v', 'Vyras'),
        ('m', 'Moteris'),
        ('p', 'Paslaptis'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=7, null=True, blank=True, unique=True)
    avatar = models.ImageField(upload_to=user_avatar_upload, null=True, blank=True)
    lytis = models.CharField(max_length=1, choices=LYTYS, default='p')
    last_read_messages = models.DateTimeField(null=True, blank=True) #2018.06.14
    bookmarks = models.ManyToManyField(Book, blank=True)

    def save(self, *args, **kwargs):
        if not self.avatar:
            super(Info, self).save(*args, **kwargs)
        else:
            self.remove_old_image_on_image_update()
            super(Info, self).save(*args, **kwargs)
    
    def remove_old_image_on_image_update(self):        
        #patikrinsim ar update ar insert
        try:
            info = Info.objects.get(user=self.user)
        except Info.DoesNotExist:
            #tokio nera, vadinasi bando insertinti
            return
        if info.avatar and self.avatar and info.avatar != self.avatar:
            info.avatar.delete()

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now, editable=False)  #auto_now_add=True
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']

    def __str__(self):
        return self.created_by.username + ': ' + self.text + ' prieš ' + self.get_age()#self.created_at.astimezone(to_tz).strftime("%Y-%m-%d %H:%M")

    def get_age(self):
        #age = datetime.now().astimezone(to_tz) - self.created_at
        age = relativedelta.relativedelta(datetime.now().astimezone(to_tz), self.created_at)

        if age.months > 0:
            return str(age.months) + ' mėn'
        elif age.days >= 10:
            return str(age.days) + ' dienas'
        elif age.days > 0 and age.days < 10:
            return str(age.days) + ' dienų'
        elif age.hours > 0:
            return str(age.hours) + ' val'
        else:
            return str(age.minutes) + ' min'

