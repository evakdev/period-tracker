# Generated by Django 3.0.8 on 2021-10-10 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_bleeding'),
    ]

    operations = [
        migrations.AddField(
            model_name='bleeding',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
