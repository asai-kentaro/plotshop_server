# Generated by Django 2.0.3 on 2018-04-06 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codeman', '0003_auto_20180324_1451'),
        ('dataman', '0002_file_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileCodeLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codeman.CodeElement')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataman.File')),
            ],
        ),
    ]
