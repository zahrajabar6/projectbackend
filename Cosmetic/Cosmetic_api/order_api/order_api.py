from Cosmetic.models import *
from Cosmetic.schemas import *
from Account.authorization import GlobalAuth
from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from django.contrib.auth import get_user_model

User = get_user_model()

Order_Router = Router(tags=['Order'])


@Order_Router.get("/cart", response={
    200: List[ItemOut],
    404: MessageOut
}, auth=GlobalAuth())
def view_cart(request):
    cart_item = Item.objects.filter(user=User.objects.get(id=request.auth['pk']), checked=False)

    if not cart_item:
        return 404, {'detail': 'No Items In The Cart,Take your time and enjoy'}
    return 200, cart_item


@Order_Router.post("/add_to_cart", response={
    200: MessageOut,
    404: MessageOut
}, auth=GlobalAuth())
def add_or_update_cart(request, item_add: CreateItem):
    try:
        item = Item.objects.get(product_id=item_add.product_id, user=User.objects.get(id=request.auth['pk']),
                                checked=False)
        if item_add.item_qty > 0:
            item.item_qty += item_add.item_qty
        item.save()
    except Item.DoesNotExist:
        if item_add.item_qty < 1:
            return 400, {'detail': 'Quantity Value Must be Greter Than Zero'}
        Item.objects.create(**item_add.dict(), user=User.objects.get(id=request.auth['pk']))
    return 200, {'detail': 'Added to cart successfully'}


@Order_Router.post("/reduce_qty", response={
    200: MessageOut,
    404: MessageOut
}, auth=GlobalAuth())
def reduce_or_delete_cart(request, item_id: int):
    try:
        item = get_object_or_404(Item, id=item_id, user=User.objects.get(id=request.auth['pk']),
                                 checked=False)
        if item.item_qty <= 1:
            item.delete()
            return 200, {'detail': 'Item deleted!'}
        item.item_qty -= 1
        item.save()

        return 200, {'detail': 'Item quantity reduced successfully!'}

    except Item.DoesNotExist:
        return 404, {'detail': 'Item DoesNotExist'}


@Order_Router.post("increase-quantity", response={
    200: MessageOut,
    404: MessageOut
}, auth=GlobalAuth())
def increase_item_qty(request, item_id: int):
    item = get_object_or_404(Item, id=item_id, user=User.objects.get(id=request.auth['pk']), checked=False)

    if not item:
        return 404, {'detail': 'Item DoesNotExist'}
    item.item_qty += 1
    item.save()
    return 200, {'detail': 'Item quantity increased successfully!'}


@Order_Router.post("/delete-item", response={
    200: MessageOut,
    404: MessageOut
}, auth=GlobalAuth())
def delete_item(request, item_id: int):
    try:
        item = get_object_or_404(Item, id=item_id, user=User.objects.get(id=request.auth['pk']),
                                 checked=False)
        item.delete()

        return 200, {'detail': 'Item deleted'}

    except Item.DoesNotExist:
        return 404, {'detail': 'Item DoesNotExist'}


@Order_Router.post("create_order", response={
    200: OrderOut,
    404: OrderOut
}, auth=GlobalAuth())
def create_order(request):
    user = User.objects.get(id=request.auth['pk'])
    user_items = user.items.filter(checked=False)
    if not user_items:
        return 404, {'user':user,
            'discounted_total': 0.00,
            'sub_total': 0.00,
            'total': 0.00,
            }
    try:
        order = user.orders.prefetch_related('items').get(checked=False)
        if order:
            order.items.set(user_items)
            order.discounted_total = order.order_total_discounted
            order.sub_total = order.order_sub_total
            order.total = ((order.sub_total + 10) - order.discounted_total)
            order.items.update(ordered=True)
            order.save()
            return 200, order
    except Order.DoesNotExist:
        order = Order.objects.create(user=user, status='NEW',
                                     checked=False)
        order.items.set(user_items)
        order.discounted_total = order.order_total_discounted
        order.sub_total = order.order_sub_total
        order.total = ((order.sub_total + 10) - order.discounted_total)
        user_items.update(ordered=True)
        order.save()
        return 200, order

@Order_Router.post('checkout', response={
    200: MessageOut,
    404: MessageOut,
    400: MessageOut,
    401: MessageOut
}, auth=GlobalAuth())
def checkout_order(request):
    user = User.objects.get(id=request.auth['pk'])
    order = Order.objects.get(user=user, checked=False)
    order.checked = True
    order.status = 'SHIPPED'
    order.save()
    user_items = user.items.filter(checked=False)
    user_items.update(checked=True)
    return 200, {'detail': 'checkout successfully!'}
