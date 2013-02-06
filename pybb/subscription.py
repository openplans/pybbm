# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import translation
from django.contrib.sites.models import Site
from django import forms

from pybb import defaults

if defaults.PYBB_USE_DJANGO_MAILER:
    try:
        from mailer import send_mail
    except ImportError:
        from django.core.mail import send_mail
else:
    from django.core.mail import send_mail


email_validator = forms.EmailField()

def notify_topic_subscribers(post):
    topic = post.topic
    if post != topic.head:
        for user in topic.subscribers.all():
            if user != post.user:
                try:
                    email_validator.clean(user.email)
                except:
                    #invalid email
                    continue
                old_lang = translation.get_language()
                lang = user.get_profile().language or settings.LANGUAGE_CODE
                translation.activate(lang)
                delete_url = reverse('pybb:delete_subscription', args=[post.topic.id])
                current_site = Site.objects.get_current()
                subject = render_to_string('pybb/mail_templates/subscription_email_subject.html',
                                           { 'site': current_site,
                                             'post': post
                                           })
                # Email subject *must not* contain newlines
                subject = ''.join(subject.splitlines())
                message = render_to_string('pybb/mail_templates/subscription_email_body.html',
                                           { 'site': current_site,
                                             'post': post,
                                             'delete_url': delete_url,
                                             })
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
                translation.activate(old_lang)


def notify_area_watchers(topic):
    from pybb.models import WatchArea

    place = topic.place
    watch_areas = WatchArea.objects.filter(fence__intersects=place).prefetch_related('watchers')
    watchers = {}

    # Construct a mapping from user primary key to a tuple of
    # (user, [watch areas that contain this topic]).
    for watch_area in watch_areas:
        users = watch_area.watchers.all()
        for user in users:
            if user.pk in watchers:
                watchers[user.pk][1].append(watch_area)
            else:
                watchers[user.pk] = (user, [watch_area])

    for user, watch_areas in watchers.itervalues():
        if user != topic.user:
            try:
                email_validator.clean(user.email)
            except:
                #invalid email
                continue
            old_lang = translation.get_language()
            lang = user.get_profile().language or settings.LANGUAGE_CODE
            translation.activate(lang)
            manage_url = reverse('pybb:edit_profile', args=[])
            current_site = Site.objects.get_current()
            subject = render_to_string('pybb/mail_templates/watch_area_subscription_email_subject.html',
                                       { 'site': current_site,
                                         'watch_areas': watch_areas,
                                         'topic': topic
                                       })
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            message = render_to_string('pybb/mail_templates/watch_area_subscription_email_body.html',
                                       { 'site': current_site,
                                         'topic': topic,
                                         'watch_areas': watch_areas,
                                         'manage_url': manage_url,
                                         })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
            translation.activate(old_lang)
