# Generated by Django 3.1.7 on 2021-03-05 22:45

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210304_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lp',
            name='cover_image',
            field=stdimage.models.StdImageField(upload_to='media/', verbose_name='Cover'),
        ),
    ]
