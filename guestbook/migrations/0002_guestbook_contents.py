# Generated by Django 2.2.2 on 2019-06-20 07:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('guestbook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestbook',
            name='contents',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
