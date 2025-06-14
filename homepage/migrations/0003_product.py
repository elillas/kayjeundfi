# Generated by Django 5.2.2 on 2025-06-07 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_alter_message_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('price', models.CharField(blank=True, max_length=50)),
                ('image_url', models.URLField(blank=True, max_length=2083)),
                ('affiliate_link', models.URLField(max_length=2083)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Products',
                'ordering': ('-date_added',),
            },
        ),
    ]
