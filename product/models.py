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
        # Generar thumbnail solo si hay imagen y no existe el thumbnail aún
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
        # Abrimos la imagen original
        img = Image.open(image)
        
        # Convertimos a RGB para evitar errores con archivos PNG o nombres extraños
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img.thumbnail(size)
        
        # Guardamos el resultado en memoria
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        # Creamos un archivo de contenido para Django
        name = image.name.replace('uploads/', '') # Limpiamos el nombre
        thumbnail = ContentFile(thumb_io.getvalue(), name=name)
        
        return thumbnail
