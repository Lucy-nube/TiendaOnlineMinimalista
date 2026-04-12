import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def save(self, *args, **kwargs):
        # Si hay imagen pero no thumbnail, lo creamos antes de guardar
        if self.image and not self.thumbnail:
            self.thumbnail = self.make_thumbnail(self.image)
        super().save(*args, **kwargs)

    def get_image(self):
        if self.image:
            return self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        if self.image:
            return self.image.url
        return ''

    def make_thumbnail(self, image, size=(300, 200)):
        # Abrir imagen
        img = Image.open(image)
        
        # Forzar modo RGB para evitar errores de transparencia en JPEG
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img.thumbnail(size)
        
        # Guardar en memoria técnica BytesIO
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        # Limpiar el nombre: quitar ruta y asegurar extensión .jpg única
        original_name = os.path.basename(image.name)
        name_only = os.path.splitext(original_name)[0]
        clean_name = f"{name_only}_thumb.jpg"
        
        return ContentFile(thumb_io.getvalue(), name=clean_name)
