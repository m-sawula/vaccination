# Generated by Django 3.0.8 on 2020-07-22 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vax', '0012_auto_20200722_0612'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaxProgramName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vax_program_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='vaxprogram',
            name='vax_program_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vax.VaxProgramName'),
        ),
    ]
