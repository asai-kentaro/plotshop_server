# Generated by Django 2.0.3 on 2018-05-11 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataman', '0006_datachank_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='remark',
            field=models.CharField(max_length=256),
        ),
    ]
