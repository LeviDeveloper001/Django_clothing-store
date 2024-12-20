from django.db import models

class Product(models.Model):
    name=models.CharField(max_length=100, blank=False)
    description=models.TextField(max_length=1000, blank=False)
    # article_number=models.IntegerField(unique=True, blank=False, auto_created=True)

    creation_date=models.DateTimeField(blank=False, auto_now_add=True)
    price=models.IntegerField(blank=False)
    seller=models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, blank=False)
    



class ProductImage(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    image_number=models.IntegerField(blank=False)
    is_main_image=models.BooleanField(default=False)
    image=models.ImageField(upload_to='static/images/product_images/', blank=False)





class ShoppingCartProduct(models.Model):
    shopping_cart=models.ForeignKey('ShoppingCart', on_delete=models.CASCADE, blank=False)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, blank=False)

    def get_price(self):
        return self.product.price


class ShoppingCartManager(models.Manager):
    pass

class ShoppingCart(models.Model):
    buyer=models.OneToOneField('accounts.Profile', on_delete=models.CASCADE, blank=False)

    objects=ShoppingCartManager()
    manager=ShoppingCartManager()

    def get_full_price(self):
        shopping_cart_products=ShoppingCartProduct.objects.filter(
            shopping_cart=self
        )
        full_price=0
        for product in shopping_cart_products:
            full_price+=product.get_price()
        return full_price


