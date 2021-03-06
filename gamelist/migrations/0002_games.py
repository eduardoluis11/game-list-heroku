# Generated by Django 4.0.1 on 2022-02-02 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamelist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('console', models.CharField(default='', max_length=64)),
                ('store', models.CharField(default='', max_length=64)),
                ('user_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='list_of_games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
