from Account.authorization import GlobalAuth
from Cosmetic.models import *
from Cosmetic.schemas import *
from django.db.models import Q
from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

Product_Router = Router(tags=['Product'])


@Product_Router.get("/list-products", response={
    200: List[ProductOut],
    404: MessageOut
})
def all_products(request, *,
                 query: str = None,
                 price_from: int = None,
                 price_to: int = None,
                 ascending: str = None,
                 descending: str = None,
                 abc: str = None,
                 cba: str = None,
                 ):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand')
    if not products:
        return 404, {'detail': 'No Products found'}
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(brand__brand_name__icontains=query)
        )

    if price_from:
        products = products.filter(price__gte=price_from)

    if price_to:
        products = products.filter(price__lte=price_to)

    if ascending:
        products = products.order_by('price')

    if descending:
        products = products.order_by('-price')
    if abc:
        products = products.order_by('name')

    if cba:
        products = products.order_by('-name')

    return products


@Product_Router.get(f"/products", response={
    200: List[ProductOut],
    404: MessageOut
})
def product(request, product_id: int):
    products = Product.objects.filter(id=product_id).select_related('category', 'brand')
    if not products:
        return 404, {'detail': f'Product with id {product_id} does not exist'}
    return products


@Product_Router.get(f"/list_favorite", response={
    200: List[FavoriteOut],
    404: MessageOut
}, auth=GlobalAuth())
def list_favorite(request):
    user = User.objects.get(id=request.auth['pk'])
    favorites = Favorite.objects.filter(user=user)
    if not favorites:
        return 404, {'detail': 'No favorites found'}
    return favorites


@Product_Router.post(f"/add_favorite", response={
    200: MessageOut,
    400: MessageOut

}, auth=GlobalAuth())
def add_favorite(request, product_id: int):
    user = User.objects.get(id=request.auth['pk'])
    fa = user.favorites.all().filter(product_id=product_id)
    if fa:
        return 400, {'detail': f'Product with id {product_id} was in favorite'}

    favorite_in = Favorite.objects.create(product_id=product_id, user=user)
    favorite_in.save()
    return 200, {'detail': f'Product with id {product_id} add to favorite'}


@Product_Router.delete(f"/Remove_favorite", response={
    200: MessageOut,
    404: MessageOut
}, auth=GlobalAuth())
def remove_favorite(request, product_id: int):
    user = User.objects.get(id=request.auth['pk'])
    fa = user.favorites.all().filter(product_id=product_id)
    if fa:
        fa = get_object_or_404(Favorite, product_id=product_id, user=user)
        fa.delete()
        return 200, {'detail': f'Product with id {product_id} remove from favorite'}
    return 404, {'detail': f'Product with id {product_id} was not in favorite'}

@Product_Router.get("is_favorites", response={
    200: IsFavorite,
    400: IsFavorite
}, auth=GlobalAuth())
def is_favorites(request, product_id: int):
    try:
        product = Favorite.objects.get(product_id=product_id, user=User.objects.get(id=request.auth['pk']))
        if product:
            return 200, {'is_favorite': 'true'}
    except Favorite.DoesNotExist:
        return 200, {'is_favorite': 'false'}

