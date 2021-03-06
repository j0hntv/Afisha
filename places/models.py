from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Title', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    description_short = models.TextField('Short description')
    description_long = HTMLField('Long description')
    latitude = models.FloatField('Latitude')
    longitude = models.FloatField('Longitude')

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Image', upload_to='place_images/')
    sort = models.PositiveIntegerField(default=0, blank=False, null=False)

    def get_preview(self):
        return format_html(f'<img src="{self.image.url}" width="150" />')

    def __str__(self):
        return f'{self.id} {self.place.title}'

    class Meta:
        ordering = ('sort',)
