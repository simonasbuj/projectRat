from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from library.models import Writer
to_tz = timezone.get_default_timezone()


# Create your models here.
class Wish(models.Model):
    STATUS_CHOICES = (
        ('n', 'new'),
        ('c', 'closed'),
        ('s', 'successful'),
        ('o', 'open')
    )
    title = models.CharField(max_length=100)
    publish_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    writers = models.ManyToManyField(Writer)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)  #auto_now_add=True
    opened_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishes'
        ordering = ['-created_at']
        verbose_name_plural = "wishes"

    def __str__(self):
        #if self.status == 'n':
        return self.title + " by " + self.created_by.username + " | " + self.get_status_display() + "(" + str(self.created_at.astimezone(to_tz)) + ")"
