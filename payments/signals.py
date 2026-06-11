from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.tasks import send_order_confirmation_email

from .models import Payment, PaymentStatus


@receiver(post_save, sender=Payment)
def send_order_confirmation_after_successful_payment(
    sender,
    instance,
    created,
    **kwargs,
):
    if created and instance.status == PaymentStatus.SUCCESS:
        send_order_confirmation_email.delay(instance.order.id)