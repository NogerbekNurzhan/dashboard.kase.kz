# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.db import migrations

def forwards_func(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    content_type = ContentType.objects.get_for_model(User)
    db_alias = schema_editor.connection.alias
    Permission.objects.using(db_alias).bulk_create([
        Permission(codename='view_user', name=' Can view users', content_type=content_type),
        Permission.objects.get_or_create(codename='change_user_password', name=' Can change user password', content_type=content_type)
    ])

class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunPython(forwards_func),
    ]
