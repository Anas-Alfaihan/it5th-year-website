# Generated by Django 4.1.4 on 2023-07-08 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_rename_islastmodifiedbyotherside_adjectivechange_isoffline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatch',
            name='lastReportDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
