from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    # Sobreescribimos el método save para generar el thumbnail una sola vez
    def save(self, *args, **kwargs):
        if self.image and not self.thumbnail:
            self.thumbnail = self.make_thumbnail(self.image)
        super().save(*args, **kwargs)

    def get_image(self):
        return self.image.url if self.image else ''

    def get_thumbnail(self):
        return self.thumbnail.url if self.thumbnail else (self.image.url if self.image else '')

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        return File(thumb_io, name=image.name)
