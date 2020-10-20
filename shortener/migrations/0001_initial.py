# Generated by Django 3.1.2 on 2020-10-19 21:30

from django.db import migrations, models
import shortener.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URLRedirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_link', models.CharField(default=shortener.models.prefix_generator, max_length=32, unique=True)),
                ('url', models.URLField(max_length=1024)),
                ('visit_count', models.IntegerField(default=0)),
            ],
        ),
    ]