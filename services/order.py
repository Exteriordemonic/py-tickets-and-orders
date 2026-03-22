from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession
from django.db import transaction


user = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict], username: str, date: str = datetime.now()
) -> Order:
    db_user = user.objects.get(username=username)

    order = Order.objects.create(user=db_user)
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


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if not username:
        return Order.objects.all()

    return Order.objects.select_related("user").filter(user__username=username)
