from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.TextField(null=False)
    metadata = models.JSONField(null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    resource_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    resource_id = models.BigIntegerField(null=True)
    resource = GenericForeignKey("resource_type", "resource_id")
    resource_name = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'audit_logs'
