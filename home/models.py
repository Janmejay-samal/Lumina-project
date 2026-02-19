from django.db import models
from django.urls import reverse

class Student(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    sec=models.CharField(max_length=10)
    branch=models.CharField(max_length=10)


class register(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    password=models.CharField(max_length=20)

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('laptops', 'Laptops'),
        ('audio', 'Audio'),
        ('wearables', 'Wearables'),
        ('accessories', 'Accessories'),
        ('limited', 'Limited Edition'),
    ]
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='laptops')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_new = models.BooleanField(default=False)
    is_limited = models.BooleanField(default=False)
    
    # Specifications
    spec_1 = models.CharField(max_length=100, blank=True)
    spec_2 = models.CharField(max_length=100, blank=True)
    spec_3 = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_category_display_name(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def get_category_class(self):
        """Returns category classes for filtering"""
        categories = [self.category]
        if self.is_limited:
            categories.append('limited')
        if self.is_new:
            categories.append('new')
        return ' '.join(categories)
    
    def get_badge(self):
        if self.is_new:
            return 'NEW'
        elif self.is_limited:
            return 'LIMITED'
        return ''