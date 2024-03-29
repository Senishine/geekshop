from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Product


class BasketQuerySet(models.QuerySet):
   def delete(self, *args, **kwargs):
       for obj in self:
           obj.product.quantity += obj.quantity
           obj.product.save()
       super(BasketQuerySet, self).delete()


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )
    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True
    )

    is_active = models.BooleanField(verbose_name='активна', default=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first().select_related()

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = self.get_items_cached
        _total_quantity = sum(map(lambda x: x.quantity, _items))
        return _total_quantity

    @property
    def total_cost(self):
        _items = self.get_items_cached
        _total_cost = sum(map(lambda x: x.product_cost, _items))
        return _total_cost

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(Basket, self).delete()

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)



