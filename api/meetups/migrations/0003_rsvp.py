# Generated by Django 2.1.7 on 2019-03-12 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetups', '0002_auto_20190311_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rsvp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('response', models.CharField(choices=[('Y', 'Yes'), ('N', 'No'), ('M', 'Maybe')], max_length=1)),
                ('meetup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetups.Meetup')),
                ('responser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]