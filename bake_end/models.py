from datetime import datetime

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.urls import reverse
from django.utils.text import slugify

from bake_end import settings


def product_image(instance, filename):
    return f'{settings.MEDIA_ROOT}/images/{instance.slug}.jpg'


def user_images(instance, filename):
    date_time = datetime.now().strftime("%Y_%m_%d,%H:%M:%S")
    saved_file_name = instance.user.username + "-" + date_time + ".jpg"
    return 'profile/{0}/{1}'.format(instance.user.username, saved_file_name)


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).get_queryset().filter(is_available=True, quantity__gte=1)


class Coordinates(models.Model):
    url = models.URLField()
    lon = models.FloatField()
    lat = models.FloatField()


class Bakery(models.Model):
    name = models.CharField(max_length=600)
    coordinates = Coordinates()


class Client(models.Model):
    name = models.CharField(max_length=600)
    email = models.EmailField()
    coordinates = Coordinates()
    birthDate = models.DateTimeField()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Livreur(Client):
    pass


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=200, db_index=True, default='none')
    categories = models.ManyToManyField(Category, related_name='products') # *categories
    price = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField()
    objects = models.Manager()
    available = AvailableManager()
    image = models.ImageField(upload_to=product_image)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:render_product', kwargs={'id': self.id,
                                                         'product_slug': self.slug,
                                                         'category_slug': self.category.slug})


class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)  # cannot create cart without client
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    def add_amount(self):
        amount = self.product.price * self.quantity
        profile = self.user.profile
        profile.total_price = profile.total_price + amount
        profile.save()
        return True


class Order(models.Model):
    livreur = models.ForeignKey(Livreur, on_delete=models.DO_NOTHING)
    coordinates = Coordinates()
    updated = models.DateTimeField(auto_now=True)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    paid = models.DateTimeField(null=True)

    def client(self):
        return self.cart.client

    def __str__(self):
        return self.livreur.name + " delivers " + ", ".join([p.name for p in self.cart.products.all()]) + " to " + self.client.name


@receiver(post_delete, sender=Client)
def profile_image_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(True)


@receiver(post_delete, sender=Product)
def product_image_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(True)
