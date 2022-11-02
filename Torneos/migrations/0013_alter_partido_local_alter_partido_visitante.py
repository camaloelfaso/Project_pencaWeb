# Generated by Django 4.1.2 on 2022-10-29 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Torneos', '0012_torneo_clasificanxgrupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partido',
            name='local',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Partido_local', to='Torneos.equipo'),
        ),
        migrations.AlterField(
            model_name='partido',
            name='visitante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Partido_visitante', to='Torneos.equipo'),
        ),
    ]
