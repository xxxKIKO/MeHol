# Generated by Django 3.2.17 on 2023-05-11 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0006_citas_cobrada'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentapaciente',
            name='idCita',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='consultas.citas'),
        ),
    ]