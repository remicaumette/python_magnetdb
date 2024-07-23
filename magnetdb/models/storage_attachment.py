from django.db import models


class StorageAttachment(models.Model):
    id = models.BigAutoField(primary_key=True)
    filename = models.CharField(max_length=255, null=True)
    content_type = models.CharField(max_length=255, null=True)
    key = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'storage_attachments'
