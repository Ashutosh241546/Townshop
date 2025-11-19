from django.db import models
from market.models import Category, SubCategory


# class Jewellery(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='mamatajwells/', blank=True, null=True)
#     is_featured = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
# class Jewellery(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='mamatajwells/', blank=True, null=True)
#     is_featured = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     # 🔥 New fields
#     category = models.ForeignKey(
#         JewelleryCategory,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="jewellery_items"
#     )

#     subcategory = models.ForeignKey(
#         JewellerySubCategory,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="jewellery_items"
#     )

#     def __str__(self):
#         return self.name



    
class Jewellery(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='mamatajwells/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 Use Existing Category Model (type='jwells')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'type': 'jwells'}
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
   
    def __str__(self):
        return self.name
   
