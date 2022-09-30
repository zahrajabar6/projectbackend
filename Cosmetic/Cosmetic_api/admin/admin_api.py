from django.shortcuts import get_object_or_404
from Account.authorization import GlobalAuth
from Cosmetic.models import Product
from Cosmetic.schemas import ProductIn, ProductOut, MessageOut, ProductUpdate
from ninja import Router
from django.contrib.auth import get_user_model

User = get_user_model()

Admin_Router = Router(tags=['Admin'])


@Admin_Router.post('create-product', response=ProductOut,
                   auth=GlobalAuth())
def create_product(request, product_in: ProductIn):
    product = Product.objects.create(**product_in.dict())
    product.save()
    return product


@Admin_Router.put(f"/update_product", response={
    200: ProductOut,
    404: MessageOut
}, auth=GlobalAuth())
def update_product(request, product_in: ProductUpdate):
    product = get_object_or_404(Product, id=product_in.id)
    for k, v in ProductUpdate.dict().items():
        setattr(product, k, v)
    product.save()
    return 200, {'detail': f'Product with id {product_in.id} was updated'}


@Admin_Router.delete(f"/delete_product", response={
    200: MessageOut,
    404: MessageOut
}, auth=GlobalAuth())
def delete_product(request, product_id: int):
    product = Product.objects.filter(id=product_id).select_related('category', 'brand')
    if not product:
        return 404, {'detail': f'Product with id {product_id} does not exist'}
    product.delete()
    return 200, {'detail': f'Product with id {product_id} was deleted'}
