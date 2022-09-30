from decimal import Decimal
from typing import List

from ninja import Schema
from django.contrib.auth import get_user_model

from Account.schemas import AccountOut

User = get_user_model()


class MessageOut(Schema):
    detail: str


class CategoryIn(Schema):
    parent_id: int
    name: str
    description: str = None
    is_active: bool


class BrandOut(Schema):
    id: int
    brand_name: str


class CategoryOut(Schema):
    id: int
    parent: 'CategoryOut' = None
    name: str
    is_active: bool


CategoryOut.update_forward_refs()


class ProductIn(Schema):
    name: str
    description: str = None
    ingredient: str = None
    price: Decimal
    discounted_price: Decimal = None
    color: str
    imageUrl: str
    category_id: int = None
    brand_id: int = None
    is_active: bool


class ProductUpdate(ProductIn):
    id: int
    name: str
    description: str = None
    ingredient: str = None
    price: Decimal
    discounted_price: Decimal = None
    color: str
    imageUrl: str
    category_id: int = None
    brand_id: int = None
    is_active: bool


class ProductOut(ProductIn):
    id: int
    name: str
    description: str = None
    ingredient: str = None
    price: Decimal
    discounted_price: Decimal = None
    color: str
    imageUrl: str
    brand: BrandOut = None
    category: CategoryOut = None
    is_active: bool


class GeneralLedgerOut(Schema):
    category: CategoryOut
    products: List[ProductOut]


class OrderIn(Schema):
    user_id: int
    total: Decimal
    status: str
    ordered: bool
    item: str


class OrderOut(Schema):
    user: AccountOut
    discounted_total: Decimal
    sub_total: Decimal
    total: Decimal


class ItemIn(Schema):
    user_id: int
    product: str
    item_qty: int
    ordered: bool


class CreateItem(Schema):
    product_id: int
    item_qty: int


class ItemOut(Schema):
    id: int
    user: AccountOut
    product: ProductOut
    item_qty: int
    ordered: bool


class RateIn(Schema):
    product_id: int
    rate: int


class RateOut(Schema):
    product_id: int
    rate: float


class FavoriteIn(Schema):
    product_id: int
    is_favorite: bool


class FavoriteOut(Schema):
    user: AccountOut
    product: ProductOut

class IsFavorite(Schema):
    is_favorite: str
