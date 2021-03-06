# Generated by Django 3.0.8 on 2020-07-12 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vax', '0004_auto_20200712_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaxCycleName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vax_cycle_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='VaxName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vax_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='VaxProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vax_program_name', models.CharField(max_length=64)),
                ('year', models.IntegerField()),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vax.Child')),
            ],
        ),
        migrations.CreateModel(
            name='VaxCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vax.VaxCycleName')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vax.VaxProgram')),
            ],
        ),
        migrations.CreateModel(
            name='Vax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp_vax_date', models.DateField()),
                ('vax_date', models.DateField(null=True)),
                ('symptom_after_vax', models.TextField(null=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vax.VaxName')),
                ('vaxcycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vax.VaxCycle')),
            ],
        ),
    ]
