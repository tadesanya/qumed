# Generated by Django 2.0.2 on 2018-05-28 10:41

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mrn', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('address', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('address', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('scheduled', 'SCHEDULED'), ('complete', 'COMPLETE'), ('lmts', 'LMTS')], max_length=16)),
                ('notes', models.TextField()),
                ('date_referred', models.DateField(auto_now_add=True)),
                ('reason_for_referral', models.CharField(max_length=128)),
                ('first_attempt', models.DateTimeField(blank=True, null=True)),
                ('second_attempt', models.DateTimeField(blank=True, null=True)),
                ('third_attempt', models.DateTimeField(blank=True, null=True)),
                ('appointment_date', models.DateTimeField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='referral.Patient')),
                ('referred_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_referrals', to='referral.Practice')),
                ('referred_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incoming_referrals', to='referral.Practice')),
            ],
        ),
    ]
