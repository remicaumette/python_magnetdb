from django.db import models


class Magnet(models.Model):
    class Meta:
        db_table = 'magnets'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=True)
    status = models.CharField(max_length=255, null=False)
    # cad_attachments = models.ManyToOneRel("CadAttachment", field_name="site")
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    design_office_reference = models.CharField(max_length=255, null=True)
    geometry_attachment = models.ForeignKey('StorageAttachment', on_delete=models.SET_NULL, null=True)
    # magnet_parts = models.ManyToOneRel('MagnetPart', field_name="site")
    parts = models.ManyToManyField('Part', through='MagnetPart', related_name='magnets')
    # site_magnets = models.ManyToOneRel('SiteMagnet', field_name="site")
    sites = models.ManyToManyField('Site', through='SiteMagnet', related_name='magnets')
    # simulations = models.ManyToOneRel("Simulation", field_name="site")

    def get_type(self):
        for part in self.magnet_parts:
            if part.part.type == 'helix':
                return 'helix'
            elif part.part.type == 'bitter':
                return 'bitter'
            elif part.part.type == 'supra':
                return 'supra'
