from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from boards.models import Board

class Chats(models.Model):
    """
    Model that represents club chats
    """
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(Board, related_name='+', on_delete=models.CASCADE)

    class Meta:
        ordering = ('date',)
        db_table = 'messages_chats'

    def __str__(self):
        """Unicode representation for a message model."""
        return self.message

    @staticmethod
    def send_message(from_user, to_user, message):
        """
        Handles the creation of message.
        It creates two message instances differing with only three fields.
            :user
            :conversation
            :is_read
        """
        message = message[:1000]
        current_club_message = Chats(from_user=from_user,
                                       message=message,
                                       user=from_user,
                                       conversation=to_user,
                                       is_read=True)
        current_user_message.save()
        Message(from_user=from_user,
                message=message,
                user=to_user,
                conversation=from_user).save()

        return current_user_message

    @staticmethod
    def get_conversations(club):
        """
        Returns a list of users having conversation with the `user` passed in.
        """

        conversations = Chats.objects.filter(
            club=Board.objects.filter(slug=club).values('id')).values('message').annotate(
                last=Max('date')).order_by('-last')

        # print('*' * 20)
        # print(conversations)
        # print('*' * 20)
        return conversations
        # users = []
        # for conversation in conversations:
        #     users.append({
        #         'user': User.objects.get(pk=conversation['conversation']),
        #         'last': conversation['last'],
        #         'unread': Message.objects.filter(user=user,
        #                                          conversation__pk=conversation[
        #                                             'conversation'],
        #                                          is_read=False).count(),
        #         })
        #
        # return users


class Message(models.Model):
    """
    Model that represents a message.
    """
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('date',)
        db_table = 'messages_message'

    def __str__(self):
        """Unicode representation for a message model."""
        return self.message

    @staticmethod
    def send_message(from_user, to_user, message):
        """
        Handles the creation of message.
        It creates two message instances differing with only three fields.
            :user
            :conversation
            :is_read
        """
        message = message[:1000]
        current_user_message = Message(from_user=from_user,
                                       message=message,
                                       user=from_user,
                                       conversation=to_user,
                                       is_read=True)
        current_user_message.save()
        Message(from_user=from_user,
                message=message,
                user=to_user,
                conversation=from_user).save()

        return current_user_message

    @staticmethod
    def get_conversations(user):
        """
        Returns a list of users having conversation with the `user` passed in.
        """
        conversations = Message.objects.filter(
            user=user).values('conversation').annotate(
                last=Max('date')).order_by('-last')
        users = []
        for conversation in conversations:
            users.append({
                'user': User.objects.get(pk=conversation['conversation']),
                'last': conversation['last'],
                'unread': Message.objects.filter(user=user,
                                                 conversation__pk=conversation[
                                                    'conversation'],
                                                 is_read=False).count(),
                })

        return users
