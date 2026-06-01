from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from datetime import datetime
from db.models import Order, Ticket
from django.db import transaction


@transaction.atomic
def create_order(tickets: list, username: str, date: datetime = None) -> None:
    user_instance = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user_instance)
    if date:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"]
        )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
