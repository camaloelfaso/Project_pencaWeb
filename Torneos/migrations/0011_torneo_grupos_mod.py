# Generated by Django 4.1.2 on 2022-10-29 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Torneos', '0010_torneo_grupos'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneo',
            name='grupos_mod',
            field=models.CharField(choices=[('I', 'IDA'), ('IV', 'Grupos')], default='I', max_length=2),
        ),
    ]