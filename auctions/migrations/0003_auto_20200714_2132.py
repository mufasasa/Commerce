# Generated by Django 3.0.7 on 2020-07-14 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200712_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='users', to='auctions.Listings'),
        ),
    ]
