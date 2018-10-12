from django.db.models.signals import post_save
from django.dispatch import receiver
from entertainment.models import Wish, Transaction
from django.utils import timezone

from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@receiver(post_save, sender=Wish)
def refund(sender, instance, **kwargs):
    if instance.status == 'c':
        transactions = instance.transaction_set.filter(is_refunded=False)
        print(instance.admin_comment)
        for t in transactions:
            response = stripe.Refund.create(
                charge = t.charge_id,
                metadata = {'reason': str(instance.admin_comment)},
            )
            if response:
                t.is_refunded = True
                t.refunded_at = timezone.now()
                t.save()


@receiver(post_save, sender=Transaction)
def check_if_enough_paid(sender, instance, **kwargs):
    #check if all transactions = wish.price
    if not instance.is_refunded:
        wish = instance.wish
        if(wish.get_transaction_sum >= wish.price):
            wish.status = 's'
            wish.save()
