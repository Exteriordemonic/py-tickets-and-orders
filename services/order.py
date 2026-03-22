from datetime import datetime
from django.db.models import QuerySet
from db.models import Order, Ticket, User, MovieSession
from django.db import transaction


def create_order(
    tickets: list[dict], username: str, date: str = datetime.now()
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)
        order.created_at = date
        order.save(update_fields=["created_at"])
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket.get("movie_session")
                ),
                order=order,
                row=ticket.get("row"),
                seat=ticket.get("seat"),
            )


def get_orders(username: str | None = None) -> QuerySet:
    if not username:
        return Order.objects.all()

    return Order.objects.select_related("user").filter(user__username=username)
