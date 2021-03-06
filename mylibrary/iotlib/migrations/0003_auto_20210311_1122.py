# Generated by Django 3.1.7 on 2021-03-11 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iotlib', '0002_auto_20210311_0902'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='picture_path',
            new_name='picture',
        ),
        migrations.RenameField(
            model_name='historicalbook',
            old_name='picture_path',
            new_name='picture',
        ),
        migrations.AlterField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('AV', 'Available'), ('OH', 'On hold'), ('MS', 'Missing'), ('IS', 'In storage')], default='IS', max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalbook',
            name='status',
            field=models.CharField(choices=[('AV', 'Available'), ('OH', 'On hold'), ('MS', 'Missing'), ('IS', 'In storage')], default='IS', max_length=255),
        ),
    ]
