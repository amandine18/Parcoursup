# Generated by Django 5.1.1 on 2024-10-24 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecole', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offres',
            name='ecole',
        ),
        migrations.RemoveField(
            model_name='offres',
            name='niveau',
        ),
        migrations.DeleteModel(
            name='Candidatures',
        ),
        migrations.DeleteModel(
            name='Ecole',
        ),
        migrations.DeleteModel(
            name='Niveaux',
        ),
        migrations.DeleteModel(
            name='Offres',
        ),
    ]
