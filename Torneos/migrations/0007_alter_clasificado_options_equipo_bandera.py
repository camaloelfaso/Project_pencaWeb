# Generated by Django 4.1.2 on 2022-10-27 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Torneos', '0006_alter_partido_options_clasificado_activo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clasificado',
            options={'ordering': ['grupo']},
        ),
        migrations.AddField(
            model_name='equipo',
            name='bandera',
            field=models.ImageField(blank=True, null=True, upload_to='PencaWeb/static/equipos_foto'),
        ),
    ]
