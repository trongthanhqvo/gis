from django.db import models
import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os
from sqlalchemy import *
from geo.Geoserver import Geoserver
from dotenv import load_dotenv
load_dotenv()

# Create your models here.


# Initializing Geoserver

geo = Geoserver('http://127.0.0.1:8080/geoserver', username=os.getenv('GEOSERVER_CONNECTION_ADMIN'), password=os.getenv('GEOSERVER_CONNECTION_PASSWORD'))


# The Tiff model
class Tiff(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to='%Y/%m/%d')
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Tiff)
def publish_data(sender, instance, created, **kwargs):
    file = instance.file.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name
    

   

 #  Publish  raster to geoserver using geoserver-rest
   
    geo.create_coveragestore(file, workspace='geoapp', lyr_name=name)

    geo.create_coveragestyle(file, style_name=name, workspace='geoapp')

    geo.publish_style(layer_name=name, style_name=name, workspace='geoapp')



@receiver(post_delete, sender=Tiff)
def delete_data(sender, instance, **kwargs):
    geo.delete_layer(instance.name, 'geoapp')


