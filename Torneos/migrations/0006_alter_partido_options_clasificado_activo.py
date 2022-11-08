# Generated by Django 4.1.2 on 2022-10-24 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Torneos', '0005_alter_torneo_fase'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partido',
            options={'ordering': ['fecha', 'torneo']},
        ),
        migrations.AddField(
            model_name='clasificado',
            name='activo',
            field=models.BooleanField(default=False),
        ),
    ]