from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, null=False)
    email = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=255, default='guest', null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    api_key = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'users'
