# Generated by Django 2.1.3 on 2019-04-29 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contabilita', '0005_remove_protocollo_select'),
    ]

    operations = [
        migrations.AddField(
            model_name='protocollo',
            name='select',
            field=models.BooleanField(default=False),
        ),
    ]