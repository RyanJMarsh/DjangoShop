from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
      title = models.CharField(max_length=100)
      slug = models.SlugField(max_length=50)

      def __str__(self):
            return self.title

      class Meta:
            verbose_name_plural= "Categories"
            ordering = ["title"]

class Item(models.Model):
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS_CHOICES = (
          (DRAFT, 'Draft'),
          (WAITING_APPROVAL, 'Waiting Approval'),
          (ACTIVE, 'Active'),
          (DELETED, 'Deleted')

    )

    user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/item_images/', blank=True, null=True)
    price= models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
            return self.title
    
    class Meta:
          ordering = ('-created_at',)

class Order(models.Model):
      created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
      first_name = models.CharField(max_length=255)
      last_name = models.CharField(max_length=255)
      address = models.CharField(max_length=255)
      total_cost = models.DecimalField(decimal_places=2, max_digits=10)
      is_paid = models.BooleanField(default=False)
      payment_intent = models.CharField(max_length=255)
      created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
      order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
      item = models.ForeignKey(Item, related_name='items', on_delete=models.CASCADE)
      price = models.DecimalField(decimal_places=2, max_digits=10)
      quantity = models.IntegerField(default=1)