# Generated by Django 4.1.7 on 2023-04-03 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_remove_dispatch_dispatchbegindate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatch',
            name='languageCourseDurationDay',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='dispatch',
            name='languageCourseDurationMonth',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='dispatch',
            name='languageCourseDurationYear',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
