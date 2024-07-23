from django.db import models


class Site(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=True)
    status = models.CharField(max_length=255, null=False)
    config_attachment = models.ForeignKey('StorageAttachment', on_delete=models.SET_NULL, null=True)
    records = models.ManyToManyField('Record', related_name='site_records')
    site_magnets = models.ManyToManyField('SiteMagnet', related_name='site_site_magnets')
    magnets = models.ManyToManyField('Magnet', through='SiteMagnet')
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'sites'
