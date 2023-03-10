# Generated by Django 4.1.4 on 2022-12-27 22:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_nominaitiondecision_nominationdecision_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adjectivechange',
            old_name='adjective',
            new_name='adjectiveChangeAdjective',
        ),
        migrations.RenameField(
            model_name='adjectivechange',
            old_name='decisionDate',
            new_name='adjectiveChangeDecisionDate',
        ),
        migrations.RenameField(
            model_name='adjectivechange',
            old_name='decisionNumber',
            new_name='adjectiveChangeDecisionNumber',
        ),
        migrations.RenameField(
            model_name='adjectivechange',
            old_name='decisionType',
            new_name='adjectiveChangeDecisionType',
        ),
        migrations.RenameField(
            model_name='adjectivechange',
            old_name='reason',
            new_name='adjectiveChangeReason',
        ),
        migrations.RenameField(
            model_name='certificateofexcellence',
            old_name='degree',
            new_name='certificateOfExcellenceDegree',
        ),
        migrations.RenameField(
            model_name='certificateofexcellence',
            old_name='year',
            new_name='certificateOfExcellenceYear',
        ),
        migrations.RenameField(
            model_name='graduatestudies',
            old_name='average',
            new_name='graduateStudiesAverage',
        ),
        migrations.RenameField(
            model_name='graduatestudies',
            old_name='college',
            new_name='graduateStudiesCollege',
        ),
        migrations.RenameField(
            model_name='graduatestudies',
            old_name='degree',
            new_name='graduateStudiesDegree',
        ),
        migrations.RenameField(
            model_name='graduatestudies',
            old_name='section',
            new_name='graduateStudiesSection',
        ),
        migrations.RenameField(
            model_name='graduatestudies',
            old_name='specialzaion',
            new_name='graduateStudiesSpecialzaion',
        ),
        migrations.RenameField(
            model_name='graduatestudies',
            old_name='university',
            new_name='graduateStudiesUniversity',
        ),
        migrations.RenameField(
            model_name='graduatestudies',
            old_name='year',
            new_name='graduateStudiesYear',
        ),
        migrations.RenameField(
            model_name='nominationdecision',
            old_name='decisionDate',
            new_name='nominationDecisionDate',
        ),
        migrations.RenameField(
            model_name='nominationdecision',
            old_name='decisionNumber',
            new_name='nominationDecisionNumber',
        ),
        migrations.RenameField(
            model_name='nominationdecision',
            old_name='decisionType',
            new_name='nominationDecisionType',
        ),
        migrations.RenameField(
            model_name='universitydegree',
            old_name='average',
            new_name='universityDegreeAverage',
        ),
        migrations.RenameField(
            model_name='universitydegree',
            old_name='section',
            new_name='universityDegreeSection',
        ),
        migrations.RenameField(
            model_name='universitydegree',
            old_name='university',
            new_name='universityDegreeUniversity',
        ),
        migrations.RenameField(
            model_name='universitydegree',
            old_name='year',
            new_name='universityDegreeYear',
        ),
        migrations.AlterField(
            model_name='demonstrator',
            name='telephone',
            field=models.CharField(blank=True, max_length=25, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{3}[-]?[0-9]{7}$', 'accept only landline numbers')]),
        ),
    ]
