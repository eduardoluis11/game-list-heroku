# Generated by Django 4.0.1 on 2022-02-02 20:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('gamelist', '0002_games'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
