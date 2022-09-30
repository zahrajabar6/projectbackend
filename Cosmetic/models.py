from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderStatusChoices(models.TextChoices):
    NEW ='NEW','New'
    PROCESSING = 'PROCESSING','Peoceeing'
    SHIPPED = 'SHIPPED','Shipped'
    COMPLETED = 'COMPLETED','Completed'
    REFUNDED = 'REFUNDED','Refunded'

class Product(models.Model):
    name = models.CharField(verbose_name='Product_Name', max_length=255)
    description = models.TextField('description', null=True, blank=True)
    ingredient = models.TextField('ingredient', null=True, blank=True)
    price = models.DecimalField('price', max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField('discounted price', max_digits=10, decimal_places=2,
                                           null=True,blank=True,default= 0)
    color = models.CharField('color',max_length = 80)
    imageUrl = models.URLField('imageUrl',max_length=255, null=True , blank=True)
    category = models.ForeignKey('Category', verbose_name='category', related_name='products',
                                 null=True,blank=True,
                                 on_delete=models.SET_NULL)
    brand = models.ForeignKey('Brand',on_delete=models.SET_NULL,related_name='products',
                                 null=True,blank=True)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)
    is_active = models.BooleanField('is active')
    def __str__(self):
        return f'{self.name}-{self.category}-{self.color}'


class Favorite(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='favorites', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', related_name='favorites',
                                on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user}-{self.product}'

class Category(models.Model):
    parent = models.ForeignKey('self',verbose_name='parent',related_name='children',null=True,blank=True,
                               on_delete=models.CASCADE)
    name = models.CharField('name', max_length=255)
    description = models.TextField('description',null=True , blank=True)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)
    is_active = models.BooleanField('is active')

    def __str__(self):
        if self.parent:
            return f'{self.parent}-{self.name}'
        return f'{self.name}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Brand(models.Model):
    brand_name = models.CharField(verbose_name='brand_name',max_length=200)

    def __str__(self):
        return self.brand_name

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='orders', null=True, blank=True,
                             on_delete=models.CASCADE)
    discounted_total = models.DecimalField('discounted', blank=True, null=True, max_digits=1000, decimal_places=2)
    sub_total = models.DecimalField('sub_total', blank=True, null=True, max_digits=1000, decimal_places=2)
    total = models.DecimalField('total', blank=True, null=True, max_digits=1000, decimal_places=2)
    status = models.CharField('status', max_length=255, choices=OrderStatusChoices.choices)
    checked = models.BooleanField('ordered')
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)
    items = models.ManyToManyField('Item', verbose_name='items', related_name='orders')

    def str(self):
        return f'{self.user}-{self.total}'

    @property
    def order_sub_total(self):
        return sum(
            i.product.price * i.item_qty for i in self.items.all()
        )

    @property
    def order_total_discounted(self):
        return sum(
            i.product.discounted_price for i in self.items.all()
        )

class Item(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product',related_name='items',
                                on_delete=models.CASCADE)
    item_qty = models.IntegerField('item_qty')
    ordered = models.BooleanField('ordered', default=False)
    checked = models.BooleanField('checked',default=False)
    def __str__(self):
        return f'{self.user}-{self.product}-{self.item_qty}'

class Rate(models.Model):
    user = models.ForeignKey(User,verbose_name='user',related_name='rates',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='product',related_name='rates',
                                on_delete=models.CASCADE)
    rate = models.IntegerField(default= 0)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f'{self.user}-{self.product}-{self.rate}'