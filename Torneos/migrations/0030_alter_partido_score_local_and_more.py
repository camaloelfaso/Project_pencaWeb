# Generated by Django 4.1.2 on 2022-11-07 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Torneos', '0029_remove_penca_participantes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partido',
            name='score_local',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='partido',
            name='score_visitante',
            field=models.IntegerField(null=True),
        ),
    ]
