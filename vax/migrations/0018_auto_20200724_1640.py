# Generated by Django 3.0.8 on 2020-07-24 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vax', '0017_auto_20200724_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='childhealthreview',
            name='child',
        ),
        migrations.AddField(
            model_name='childhealthreview',
            name='child',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vax.Child'),
        ),
        migrations.AlterField(
            model_name='childhealthreview',
            name='exp_workup_day',
            field=models.DateField(verbose_name='Wymagana data badania'),
        ),
        migrations.AlterField(
            model_name='childhealthreview',
            name='remarks',
            field=models.TextField(verbose_name='Spostrzeżenia i zalecenia'),
        ),
        migrations.AlterField(
            model_name='childhealthreview',
            name='workup_day',
            field=models.DateField(blank=True, help_text='YYYY-MM-DD', null=True, verbose_name='Data badania'),
        ),
    ]
