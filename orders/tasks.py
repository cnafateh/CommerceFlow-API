from celery import shared_task


@shared_task
def send_order_confirmation_email(order_id):
    print(f"Order confirmation email sent for order #{order_id}")
    return f"Email sent for order #{order_id}"