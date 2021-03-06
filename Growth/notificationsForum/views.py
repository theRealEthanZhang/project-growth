# -*- coding: utf-8 -*-
''' Django notificationsForum example views '''
from distutils.version import \
    StrictVersion  # pylint: disable=no-name-in-module,import-error

from django import get_version
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from notificationsForum import settings
from notificationsForum.settings import get_config
from notificationsForum.utils import id2slug, slug2id
from swapper import load_model

NotificationForum = load_model('notificationsForum', 'NotificationForum')

if StrictVersion(get_version()) >= StrictVersion('1.7.0'):
    from django.http import JsonResponse  # noqa
else:
    # Django 1.6 doesn't have a proper JsonResponse
    import json
    from django.http import HttpResponse  # noqa

    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    def JsonResponse(data):  # noqa
        return HttpResponse(
            json.dumps(data, default=date_handler),
            content_type="application/json")


class NotificationViewList(ListView):
    template_name = 'notificationsForum/list.html'
    context_object_name = 'notificationsForum'
    paginate_by = settings.get_config()['PAGINATE_BY']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationViewList, self).dispatch(
            request, *args, **kwargs)


class AllnotificationsForumList(NotificationViewList):
    """
    Index page for authenticated user
    """

    def get_queryset(self):
        if settings.get_config()['SOFT_DELETE']:
            qset = self.request.user.notificationsForum.active()
        else:
            qset = self.request.user.notificationsForum.all()
        return qset


class UnreadnotificationsForumList(NotificationViewList):

    def get_queryset(self):
        return self.request.user.notificationsForum.unread()


@login_required
def mark_all_as_read(request):
    request.user.notificationsForum.mark_all_as_read()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)
    return redirect('notificationsForum:unread')


@login_required
def mark_as_read(request, slug=None):
    notification_id = slug2id(slug)

    notificatonForum = get_object_or_404(
        NotificationForum, recipient=request.user, id=notification_id)
    notificatonForum.mark_as_read()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    return redirect('notificationsForum:unread')

    # return redirect('/forum/')


@login_required
def mark_as_unread(request, slug=None):
    notification_id = slug2id(slug)

    notificatonForum = get_object_or_404(
        NotificationForum, recipient=request.user, id=notification_id)
    notificatonForum.mark_as_unread()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    return redirect('notificationsForum:unread')


@login_required
def delete(request, slug=None):
    notification_id = slug2id(slug)

    notificatonForum = get_object_or_404(
        NotificationForum, recipient=request.user, id=notification_id)

    if settings.get_config()['SOFT_DELETE']:
        notificatonForum.deleted = True
        notificatonForum.save()
    else:
        notificatonForum.delete()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    return redirect('notificationsForum:all')


@never_cache
def live_unread_notification_count(request):
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'unread_count': 0
        }
    else:
        data = {
            'unread_count': request.user.notificationsForum.unread().count(),
        }
    return JsonResponse(data)


@never_cache
def live_unread_notification_list(request):
    ''' Return a json with a unread notificatonForum list '''
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'unread_count': 0,
            'unread_list': []
        }
        return JsonResponse(data)

    default_num_to_fetch = get_config()['NUM_TO_FETCH']
    try:
        # If they don't specify, make it 5.
        num_to_fetch = request.GET.get('max', default_num_to_fetch)
        num_to_fetch = int(num_to_fetch)
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:  # If casting to an int fails.
        num_to_fetch = default_num_to_fetch

    unread_list = []

    for notificatonForum in request.user.notificationsForum.unread()[0:num_to_fetch]:
        struct = model_to_dict(notificatonForum)
        struct['slug'] = id2slug(notificatonForum.id)
        if notificatonForum.actor:
            struct['actor'] = str(notificatonForum.actor)
        if notificatonForum.target:
            struct['target'] = str(notificatonForum.target)
        if notificatonForum.action_object:
            struct['action_object'] = str(notificatonForum.action_object)
        if notificatonForum.data:
            struct['data'] = notificatonForum.data
        unread_list.append(struct)

        if request.GET.get('mark_as_read'):
            notificatonForum.mark_as_read()
    data = {
        'unread_count': request.user.notificationsForum.unread().count(),
        'unread_list': unread_list
    }
    return JsonResponse(data)


@never_cache
def live_all_notification_list(request):
    ''' Return a json with a unread notificatonForum list '''
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'all_count': 0,
            'all_list': []
        }
        return JsonResponse(data)

    default_num_to_fetch = get_config()['NUM_TO_FETCH']
    try:
        # If they don't specify, make it 5.
        num_to_fetch = request.GET.get('max', default_num_to_fetch)
        num_to_fetch = int(num_to_fetch)
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:  # If casting to an int fails.
        num_to_fetch = default_num_to_fetch

    all_list = []

    for notificatonForum in request.user.notificationsForum.all()[0:num_to_fetch]:
        struct = model_to_dict(notificatonForum)
        struct['slug'] = id2slug(notificatonForum.id)
        if notificatonForum.actor:
            struct['actor'] = str(notificatonForum.actor)
        if notificatonForum.target:
            struct['target'] = str(notificatonForum.target)
        if notificatonForum.action_object:
            struct['action_object'] = str(notificatonForum.action_object)
        if notificatonForum.data:
            struct['data'] = notificatonForum.data
        all_list.append(struct)
        if request.GET.get('mark_as_read'):
            notificatonForum.mark_as_read()
    data = {
        'all_count': request.user.notificationsForum.count(),
        'all_list': all_list
    }
    return JsonResponse(data)


def live_all_notification_count(request):
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'all_count': 0
        }
    else:
        data = {
            'all_count': request.user.notificationsForum.count(),
        }
    return JsonResponse(data)
