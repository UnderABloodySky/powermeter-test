# Generated by Django 4.1.5 on 2023-01-20 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('name', models.CharField(max_length=180)),
                ('meter_key', models.CharField(max_length=42, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('recorded_consumption', models.FloatField(null=True)),
                ('measurement_key', models.AutoField(primary_key=True, serialize=False)),
                ('meter_key', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='test.meter')),
            ],
        ),
    ]
