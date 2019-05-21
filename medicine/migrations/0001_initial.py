# Generated by Django 2.2 on 2019-05-21 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import medicine.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verdict', medicine.models.PatchedMultiSelectField(choices=[('high_blood_pressure', 'Hypertension causes symptoms such as headache, shortness of breath, dizziness, chest pain, heart palpitations and nosebleeds'), ('low_blood_pressure', 'Low blood pressure can cause impaired blood supply in certain parts of the brain responsible for hearing and vision, which can cause deafness and reduced vision'), ('high_glucose', 'Glucose elevation is observed when:diabetes, pancreatic tumors, stress and others.'), ('high_glucose', 'Low blood pressure can cause impaired blood supply in certain parts of the brain responsible for hearing and vision, which can cause deafness and reduced vision'), ('high_protein', 'Increased protein content in the blood is observed with: intestinal obstruction, acute and chronic infectious diseases, etc.'), ('low_protein', 'The decrease in the protein content in the blood is observed when: pancreatitis, hepatitis, injuries, etc.'), ('high_albumin', 'An increase in the level of albumin is observed when dehydration of the body'), ('low_albumin', 'The decrease in albumin level is observed when: malnutrition (insufficient intake of proteins from food), chronic liver diseases, etc'), ('high_myoglobin', 'Increased myoglobin level is observed with:injuries, convulsions, burns. Physiological elevation of myoglobin often occurs during muscle overload.'), ('low_myoglobin', 'A decrease in myoglobin level is observed when: polymyositis.'), ('high_ferritin', 'An increase in the level of ferritin is observed when: acute hepatitis.'), ('low_ferritin', 'A decrease in the level of ferritin is observed in case of iron deficiency anemia.'), ('high_temperature', 'High temperature can cause bad feeling, weakness in limbs and whole body.')], max_length=187, verbose_name='verdict')),
                ('start_time', models.DateTimeField(editable=False, verbose_name='start time')),
                ('end_time', models.DateTimeField(editable=False, verbose_name='end time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'diagnosis',
                'verbose_name_plural': 'diagnosis',
            },
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_blood_pressure', models.PositiveIntegerField(verbose_name='min pressure')),
                ('max_blood_pressure', models.PositiveIntegerField(verbose_name='max pressure')),
                ('glucose_rate', models.FloatField(verbose_name='glucose rate')),
                ('protein_rate', models.FloatField(verbose_name='protein rate')),
                ('albumin_rate', models.FloatField(verbose_name='albumin rate')),
                ('myoglobin_rate', models.FloatField(verbose_name='myoglobin rate')),
                ('ferritin_rate', models.FloatField(verbose_name='ferritin rate')),
                ('cholesterol_rate', models.FloatField(verbose_name='cholesterol rate')),
                ('temperature', models.FloatField(verbose_name='temperature')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('diagnosis', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='medicine.Diagnosis')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'statistics',
                'verbose_name_plural': 'statistics',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='reason')),
                ('description', models.TextField(verbose_name='description')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='expiration date')),
                ('time', models.TimeField(verbose_name='time')),
                ('days', medicine.models.PatchedMultiSelectField(choices=[(0, 'monday'), (1, 'tuesday'), (2, 'wednesday'), (3, 'thursday'), (4, 'friday'), (5, 'saturday'), (6, 'sunday'), (7, 'everyday')], max_length=15, verbose_name='days')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'schedule',
                'verbose_name_plural': 'schedules',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('pending', models.BooleanField(default=True, verbose_name='pending')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicine.Schedule', verbose_name='schedule')),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
            },
        ),
    ]
