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

    def save(self, *args, **kwargs):
        # Solo generamos el thumbnail si hay imagen y no existe uno previo
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
            # Si falla el thumbnail, devolvemos la imagen original por seguridad
            return self.image.url
        return ''

    def make_thumbnail(self, image, size=(300, 200)):
        # Abrir la imagen desde el almacenamiento (Cloudinary)
        img = Image.open(image)
        
        # Convertir a RGB (necesario para JPEG)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img.thumbnail(size)
        
        # Guardar en memoria
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        # Obtener el nombre base sin rutas ni extensiones extrañas
        original_name = os.path.basename(image.name)
        # Separamos nombre de extensión y forzamos .jpg
        clean_name = os.path.splitext(original_name)[0] + ".jpg"
        
        return ContentFile(thumb_io.getvalue(), name=clean_name)
