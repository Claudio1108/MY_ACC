# Generated by Django 2.1.3 on 2019-04-29 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Contabilita', '0008_auto_20190429_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protocollo',
            name='select',
        ),
    ]
