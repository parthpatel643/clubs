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

import requests

from mysite.decorators import ajax_required

from .forms import SubjectForm
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
def new_message_all(request):
    """
    Displays a form & handle action for creating new subject.
    """
    subject_form = SubjectForm(**{'user': request.user})

    if request.method == 'POST':
        subject_form = SubjectForm(request.POST, request.FILES)
        if subject_form.is_valid():
            new_message_all = subject_form.save(commit=False)
            author = request.user
            new_message_all.author = author
            new_message_all.save()
            new_message_all.points.add(author)
            new_message_all.save()

            # Checks if someone is mentioned in the subject
            words = new_message_all.title + ' ' + new_message_all.body
            words = words.split(" ")
            names_list = []
            for word in words:

                # if first two letter of the word is "u/" then the rest of the word
                # will be treated as a username

                if word[:2] == "u/":
                    u = word[2:]
                    try:
                        user = User.objects.get(username=u)
                        if user not in names_list:
                            new_message_all.mentioned.add(user)
                            if request.user is not user:
                                Notification.objects.create(
                                    Actor=new_message_all.author,
                                    Object=new_message_all,
                                    Target=user,
                                    notif_type='subject_mentioned'
                                )
                            names_list.append(user)
                    except:  # noqa: E722
                        pass

            if new_message_all.photo:
                image_compression(new_message_all.photo.name)

            return redirect(new_message_all.get_absolute_url())

    form_filling = True

    return render(request, 'notifications/new_message_all.html', {
        'subject_form': subject_form, 'form_filling': form_filling
    })


@login_required
@ajax_required
def check_activities(request):
    subject_events = Notification.objects.filter(Target=request.user, is_read=False).exclude(Actor=request.user)
    return HttpResponse(len(subject_events))
