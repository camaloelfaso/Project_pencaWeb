# Generated by Django 4.1.2 on 2022-11-01 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Torneos', '0023_clasificado_empatados_clasificado_ganados_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clasificado',
            options={'ordering': ['grupo', '-puntos']},
        ),
        migrations.AddField(
            model_name='partido',
            name='modif_ranking',
            field=models.BooleanField(default=False),
        ),
    ]
