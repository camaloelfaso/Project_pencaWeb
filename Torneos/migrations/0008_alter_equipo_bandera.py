# Generated by Django 4.1.2 on 2022-10-27 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Torneos', '0007_alter_clasificado_options_equipo_bandera'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='bandera',
            field=models.ImageField(blank=True, null=True, upload_to='equipos_foto'),
        ),
    ]
