# Generated by Django 2.1.3 on 2019-05-03 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Contabilita', '0016_protocollo_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protocollo',
            name='public',
        ),
    ]