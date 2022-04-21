# Generated by Django 3.1.2 on 2022-04-21 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('precio', models.FloatField(verbose_name='Precio')),
            ],
            options={
                'verbose_name': 'compra',
                'verbose_name_plural': 'compras',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Medicamentos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripción')),
                ('receta', models.CharField(max_length=1, verbose_name='Receta')),
                ('precio', models.FloatField(verbose_name='Precio')),
                ('stock', models.IntegerField(verbose_name='Stock')),
            ],
            options={
                'verbose_name': 'medicamento',
                'verbose_name_plural': 'médicamentos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Medicos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('apellidos', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('edad', models.IntegerField(verbose_name='Edad')),
                ('fechaalta', models.DateField(verbose_name='Fecha de alta')),
                ('especialidad', models.CharField(max_length=40, verbose_name='Especialidad')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Nombre de usuario')),
                ('password', models.CharField(max_length=30, verbose_name='Contraseña')),
            ],
            options={
                'verbose_name': 'médico',
                'verbose_name_plural': 'médicos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Pacientes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('apellidos', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('edad', models.IntegerField(verbose_name='Edad')),
                ('direccion', models.CharField(max_length=100, verbose_name='Dirección')),
                ('foto', models.ImageField(upload_to='pacientes/', verbose_name='Foto')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Nombre de usuario')),
                ('password', models.CharField(max_length=30, verbose_name='Contraseña')),
            ],
            options={
                'verbose_name': 'paciente',
                'verbose_name_plural': 'pacientes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ComprasMedicamentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idCompra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguroprivado.compras', verbose_name='Compra')),
                ('idMedicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguroprivado.medicamentos', verbose_name='Medicamento')),
            ],
        ),
        migrations.AddField(
            model_name='compras',
            name='idPaciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguroprivado.pacientes', verbose_name='Paciente'),
        ),
        migrations.CreateModel(
            name='Citas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('observaciones', models.TextField(verbose_name='Observaciones')),
                ('idMedico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguroprivado.medicos', verbose_name='Médico')),
                ('idPaciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguroprivado.pacientes', verbose_name='Paciente')),
            ],
            options={
                'verbose_name': 'cita',
                'verbose_name_plural': 'citas',
                'ordering': ['-id'],
            },
        ),
    ]
