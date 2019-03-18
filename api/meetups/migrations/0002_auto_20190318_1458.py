# Generated by Django 2.1.7 on 2019-03-18 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meetups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvp',
            name='responder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meetup',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meetup',
            name='image_url',
            field=models.ManyToManyField(to='meetups.Image'),
        ),
        migrations.AddField(
            model_name='meetup',
            name='tags',
            field=models.ManyToManyField(to='meetups.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('image_url',)},
        ),
        migrations.AlterUniqueTogether(
            name='meetup',
            unique_together={('body', 'scheduled_date', 'location'), ('title', 'scheduled_date', 'location')},
        ),
    ]