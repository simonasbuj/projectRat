from django.db.models.signals import post_save
from django.dispatch import receiver
from entertainment.models import Wish

@receiver(post_save, sender=Wish)
def refund(sender, instance, **kwargs):
    if instance.status == 'c':
        print("REFUNDINSIM CHARGUS VISUS")