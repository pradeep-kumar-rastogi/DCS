# Generated by Django 4.2.4 on 2023-08-24 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dcs_actionsforms',
            name='status',
            field=models.CharField(choices=[('In Progress', 'In Progress'), ('Done', 'Done'), ('On Hold', 'On Hold')], max_length=20),
        ),
    ]