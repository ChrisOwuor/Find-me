# Generated by Django 4.2.4 on 2023-09-13 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Find_Me_App', '0011_remove_missingperson_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportedseenperson',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
