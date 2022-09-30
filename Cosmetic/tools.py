# class City(models.Model):
#     name = models.CharField('city', max_length=255)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'city'
#         verbose_name_plural = 'cities'


# class Address(models.Model):
#     user = models.ForeignKey(User, verbose_name='user', related_name='addresses', on_delete=models.CASCADE)
#     address = models.CharField('address', max_length=255)
#     city = models.ForeignKey('City', related_name='addresses', on_delete=models.CASCADE,null=True)
#     phone = models.CharField('phone', max_length=255)
#
#     class Meta:
#         verbose_name = 'Address'
#         verbose_name_plural = 'Addresses'
#     def __str__(self):
#         return f' {self.user}-{self.address} - {self.phone}'

# class Color(models.Model):
#     productName = models.ForeignKey('Product',verbose_name='Product_Name',on_delete=models.SET_NULL,null=True)
#     color = models.CharField(max_length=50,verbose_name='Product_Color')
#     imageUrl = models.URLField(max_length=255)
#
#     def __str__(self):
#         return f'{self.productName} - {self.color}'

