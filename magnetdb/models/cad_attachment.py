from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class CadAttachment(models.Model):
    id = models.BigAutoField(primary_key=True)
    attachment = models.ForeignKey('StorageAttachment', on_delete=models.CASCADE, null=False)
    resource_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    resource_id = models.BigIntegerField(null=True)
    resource = GenericForeignKey("resource_type", "resource_id")
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'cad_attachments'
