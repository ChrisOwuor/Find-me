# Generated by Django 4.2.4 on 2023-09-09 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Find_Me_App', '0007_alter_person_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissingPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('code', models.CharField(default='LSTCXQSKPXAXA254', max_length=20)),
                ('matched', models.BooleanField(default=False)),
                ('age', models.IntegerField()),
                ('location', models.CharField(default='Nairobi', max_length=100)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.RenameModel(
            old_name='FoundPerson',
            new_name='ReportedSeenPerson',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
