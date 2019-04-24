from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.conf import settings
from django.contrib.auth.models import User
from django.db import OperationalError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from boards.models import Board
import requests

from mysite.decorators import ajax_required

from .forms import NotificationForm
from .models import Notification


class ActivitiesPageView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the activities list per user."""
    model = Notification
    paginate_by = 20
    template_name = 'notifications/activities.html'
    context_object_name = 'events'

    def get_queryset(self, **kwargs):
        subject_events = Notification.objects.filter(Target=self.request.user).exclude(Actor=self.request.user)
        # Do this with celery.
        unread_subject_events = subject_events.filter(is_read=False)
        for notification in unread_subject_events:
            notification.is_read = True
            notification.save()
        return subject_events


@login_required
def notify_all(request):
    """
    Displays a form & handle action for creating new notification.
    """
    notif_form = NotificationForm(**{'user': request.user})

    if request.method == 'POST':
        notif_form = NotificationForm(request.POST, request.FILES)
        if notif_form.is_valid():
            club = Board.objects.filter(title=notif_form.cleaned_data['board'])
            print('*' * 20)
            users = club[0].subscribers.all()
            print('*' * 20)

            for user in users:
                Notification.objects.create(
                    Actor=request.user,
                    Target=user,
                    notif_type='notify_all',
                    notif_message=notif_form.cleaned_data['title']
                )
            return redirect('/')

    form_filling = True


    return render(request, 'notifications/notify_all.html', {
        'notif_form': notif_form, 'form_filling': form_filling
    })


@login_required
@ajax_required
def check_activities(request):
    subject_events = Notification.objects.filter(Target=request.user, is_read=False).exclude(Actor=request.user)
    return HttpResponse(len(subject_events))
