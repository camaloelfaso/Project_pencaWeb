# Generated by Django 4.1.2 on 2022-10-28 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Torneos', '0008_alter_equipo_bandera'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='codigo',
            field=models.CharField(default='', max_length=10),
        ),
    ]