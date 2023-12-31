# Generated by Django 3.1.7 on 2023-09-25 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eProc_Configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('notification_id', models.CharField(db_column='NOTIFICATION_ID', max_length=32, primary_key=True, serialize=False)),
                ('username', models.CharField(db_column='USERNAME', max_length=16, null=True)),
                ('notification_type_id', models.CharField(db_column='NOTIFICATION_TYPE_ID', max_length=12)),
                ('values', models.CharField(db_column='VALUES', max_length=30)),
                ('read_status', models.BooleanField(db_column='READ_STATUS', default=False)),
                ('object_id', models.PositiveIntegerField(db_column='OBJECT_ID', null=True)),
                ('star_notif_flag', models.BooleanField(db_column='STAR_NOTIF_FLAG', default=False)),
                ('notif_created_by', models.CharField(db_column='NOTIF_CREATED_BY', max_length=30, null=True)),
                ('notif_created_at', models.DateTimeField(blank=True, db_column='NOTIF_CREATED_AT', null=True)),
                ('notif_changed_by', models.CharField(db_column='NOTIF_CHANGED_BY', max_length=30, null=True)),
                ('notif_changed_at', models.DateTimeField(blank=True, db_column='NOTIF_CHANGED_AT', null=True)),
                ('del_ind', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eProc_Configuration.orgclients')),
            ],
            options={
                'db_table': 'MTD_NOTIFICATIONS',
                'managed': True,
            },
        ),
    ]
