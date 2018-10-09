from django.db.models.signals import post_save
from django.dispatch import receiver
from entertainment.models import Wish, Transaction
from django.utils import timezone

@receiver(post_save, sender=Wish)
def refund(sender, instance, **kwargs):
    if instance.status == 'c':
        print("REFUNDINSIM CHARGUS VISUS")
        print("PRIEZASITS: " + instance.admin_comment)

@receiver(post_save, sender=Transaction)
def check_if_enough_paid(sender, instance, **kwargs):
    #TO-DO check if all transactions = wish.price
    print(instance.wish)
