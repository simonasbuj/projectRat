from django.db import models
from django.urls import reverse
from django.utils import timezone
from dateutil import relativedelta
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
    updated_at = models.DateTimeField(default=timezone.now)
    admin_comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishes'
        ordering = ['-updated_at']
        verbose_name_plural = "Lankytojų prašymai"

    def __str__(self):
        #if self.status == 'n':
        return self.title + " by " + self.created_by.username + " | " + self.get_status_display() + "(" + str(self.created_at.astimezone(to_tz)) + ")"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Wish, self).save(*args, **kwargs)

    @property
    def get_age(self):
        age = relativedelta.relativedelta(timezone.now(), self.created_at)
        return age.days

    @property
    def get_timeleft(self):
        return 30 - self.get_age

    @property
    def get_transaction_sum(self):
        t_sum = 0
        transactions = self.transaction_set.filter(is_refunded=False)
        for t in transactions:
            t_sum += t.amount

        return t_sum

    @property
    def get_goal_percent(self):
        t_sum = self.get_transaction_sum
        percent = (t_sum * 100)/self.price
        return percent

    @property
    def api_url(self):
        return reverse('api:wish-detail', kwargs={'pk':self.id})   


class Transaction(models.Model):
    charge_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    email = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    is_refunded = models.BooleanField(default=False)
    refunded_at = models.DateTimeField(null=True, blank=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    wish = models.ForeignKey(Wish, on_delete=models.PROTECT)

    class Meta:
        db_table = 'transactions'
        ordering = ['-refunded_at', '-created_at']

    def __str__(self):
        return self.wish.title

    @property
    def get_formated_date(self):
        return self.created_at.astimezone(to_tz).strftime('%Y-%m-%d %H:%M:%S')
    