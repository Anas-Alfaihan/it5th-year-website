# Generated by Django 4.1.4 on 2022-12-27 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_rename_adjective_adjectivechange_adjectivechangeadjective_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='universitydegree',
            name='universityDegreeCollege',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
