from django.db import models


class Magnet(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=True)
    status = models.CharField(max_length=255, null=False)
    cao_attachment = models.ManyToManyField("CadAttachment")
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    design_office_reference = models.CharField(max_length=255, null=True)
    geometry_attachment = models.ForeignKey('StorageAttachment', on_delete=models.SET_NULL, null=True)
    magnet_parts = models.ManyToManyField('MagnetPart', related_name='magnet_magnet_parts')
    parts = models.ManyToManyField('Part', through='MagnetPart')
    site_magnets = models.ManyToManyField('SiteMagnet', related_name='magnet_site_magnets')
    sites = models.ManyToManyField('Site', through='SiteMagnet')

    def get_type(self):
        for part in self.magnet_parts:
            if part.part.type == 'helix':
                return 'helix'
            elif part.part.type == 'bitter':
                return 'bitter'
            elif part.part.type == 'supra':
                return 'supra'

    class Meta:
        db_table = 'magnets'
