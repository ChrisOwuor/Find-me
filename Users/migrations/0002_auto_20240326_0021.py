# Generated by Django 4.2.6 on 2024-03-25 21:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    def generate_uuids(apps, schema_editor):
        if schema_editor.connection.alias != "default":
            print('default')
            return
        User = apps.get_model('Users', 'User')
        for user in User.objects.all():
            if not user.u_id:
                user.u_id = uuid.uuid4()
                user.save()

    dependencies = [
        ('Users', '0001_initial'),

    ]

    operations = [
        migrations.AddField(
            model_name='User',
            name='u_id',
            field=models.UUIDField(editable=False, default=uuid.uuid4),
        ),
        migrations.RunPython(generate_uuids),

    ]
