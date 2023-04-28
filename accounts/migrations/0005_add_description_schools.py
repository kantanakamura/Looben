# Generated by Django 4.0.6 on 2022-08-26 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_add_natinal_place_in_schools'),
    ]

    operations = [
        migrations.AddField(
            model_name='schools',
            name='address',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='schools',
            name='average_academic_fee',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='schools',
            name='average_domitary_fee',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='schools',
            name='description',
            field=models.CharField(max_length=260, null=True),
        ),
        migrations.AddField(
            model_name='schools',
            name='homepage',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='schools',
            name='number_of_students',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='schools',
            name='picture',
            field=models.FileField(blank=True, upload_to='univeristy/'),
        ),
    ]