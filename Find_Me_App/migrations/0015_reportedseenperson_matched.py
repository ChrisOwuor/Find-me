# Generated by Django 4.2.4 on 2023-09-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Find_Me_App', '0014_missingperson_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportedseenperson',
            name='matched',
            field=models.BooleanField(default=False),
        ),
    ]
