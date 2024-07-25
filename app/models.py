from django.db import models


class Product(models.Model):
    COLOR_CHOICES = [
        ('black', 'black'),
        ('white', 'white'),
        ('Red', 'red'),
        ('Green', 'green'),
        ('Blue', 'blue'),
        ('Yellow', 'yellow'),
        ('Purple', 'purple'),
        ('Orange', 'orange'),
        ('Pink', 'pink'),
        ('Teal', 'teal'),
        ('Gray', 'gray'),
        ('Brown', 'brown'), ]

    name = models.CharField(max_length=100)
    price = models.FloatField(null=False)
    description = models.TextField()
    ratings = models.IntegerField(default=0)
    favoured = models.BooleanField(default=False)
    add_to_cart = models.BooleanField(default=False)
    discount = models.FloatField(default=0.0)
    color = models.CharField(
        choices=COLOR_CHOICES,
        help_text="Select a color for the product",)

    @property
    def status(self) -> str:
        return self.price // 20

    objects = models.Manager

    class Meta:
        verbose_name_plural = "All Products"

    def get_attributes(self) -> list[dict]:
        product_attributes = AttributeReference.objects.filter(product=self)
        p_a = []
        for p in product_attributes:
            p_a.append({
                'key': p.key,
                'value': p.value
            })
        return p_a

    def get_attributes_as_dict(self) -> dict:
        attributes = self.get_attributes()
        attributes_dict = {}
        for attribute in attributes:
            attributes_dict[attribute['key']] = attribute['value']

        return attributes_dict

    @property
    def discount_price(self):
        if self.discount:
            return (1 - self.discount / 100) * self.price
        return self.price

    def __str__(self):
        return self.name


class Images(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='images')

    class Meta:
        verbose_name_plural = "All Images"


class AttributeKey(models.Model):
    key = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.key


class AttributeValue(models.Model):
    value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.value


class AttributeReference(models.Model):
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE)
    key = models.ForeignKey('app.AttributeKey', on_delete=models.CASCADE)
    value = models.ForeignKey('app.AttributeValue', on_delete=models.CASCADE)

    objects = models.Manager
