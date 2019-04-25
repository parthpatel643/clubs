# Generated by Django 2.2 on 2019-04-24 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notif_message',
            field=models.CharField(default='None', max_length=500),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.CharField(choices=[('subject_mentioned', 'Mentioned in Subject'), ('comment_mentioned', 'Mentioned in Comment'), ('comment', 'Comment on Subject'), ('follow', 'Followed by someone'), ('sent_msg_request', 'Sent a Message Request'), ('confirmed_msg_request', 'Sent a Message Request'), ('notify_all', 'Sent a Notification To Everyone')], default='Comment on Subject', max_length=500),
        ),
    ]
