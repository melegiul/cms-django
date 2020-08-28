from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.forms import formset_factory

from .push_notification_sender import PushNotificationSender
from ...decorators import region_permission_required
from ...forms.push_notifications import PushNotificationForm, PushNotificationTranslationForm
from ...models import Language, PushNotification, PushNotificationTranslation, Region


@method_decorator(login_required, name='dispatch')
@method_decorator(region_permission_required, name='dispatch')
class PushNotificationView(PermissionRequiredMixin, TemplateView):
    permission_required = 'cms.view_push_notifications'
    raise_exception = True

    template_name = 'push_notifications/push_notification_form.html'
    base_context = {'current_menu_item': 'push_notifications'}
    push_sender = PushNotificationSender()

    def get(self, request, *args, **kwargs):
        push_notification = PushNotification.objects.filter(id=kwargs.get('push_notification_id')).first()
        region = Region.objects.get(slug=kwargs.get('region_slug'))
        language = Language.objects.get(code=kwargs.get('language_code'))
        if push_notification:
            push_notification_form = PushNotificationForm(instance=push_notification)
            push_notification_translations = PushNotificationTranslation.objects.filter(
                push_notification=push_notification
            )
            push_notification_translation_formset = formset_factory(PushNotificationTranslationForm)
            push_notification_translation_formset = push_notification_translation_formset(queryset=PushNotificationTranslation.objects.filter(push_notification=push_notification).order_by(language))()
        else:
            push_notification_form = PushNotificationForm()
            push_notification_translation_formset = formset_factory(PushNotificationTranslationForm, min_num=(len(region.languages)-1))()

        formset_dict = {}
        i = 0
        for form in push_notification_translation_formset:
            language = region.languages[i]
            formset_dict[language] = form
            i = i + 1

        return render(request, self.template_name, {
            **self.base_context,
            'push_notification': push_notification,
            'formset_dict': formset_dict,
            'language': language,
            'languages': region.languages,
        })

    # pylint: disable=too-many-branches,unused-argument
    def post(self, request, *args, **kwargs):

        if not request.user.has_perm('cms.edit_push_notifications'):
            raise PermissionDenied

        if 'submit_send' in request.POST:
            if not request.user.has_perm('cms.send_push_notifications'):
                raise PermissionDenied

        region = Region.objects.get(slug=kwargs.get('region_slug'))
        language = Language.objects.get(code=kwargs.get('language_code'))

        # At first check if push notification exists already
        push_notification = PushNotification.objects.filter(id=kwargs.get('push_notification_id')).first()
        if push_notification:
            push_notification_form = PushNotificationForm(request.POST, instance=push_notification)
            success_message = _('Push notification saved successfully.')
        else:
            push_notification_form = PushNotificationForm(request.POST)
            success_message = _('Push notification created successfully.')

        # Then check if translation in current language already exists
        push_notification_translation = PushNotificationTranslation.objects.filter(
            push_notification=push_notification,
            language=language
        )
        if push_notification_translation.exists():
            push_notification_translation_form = PushNotificationTranslationForm(
                request.POST,
                instance=push_notification_translation.first()
            )
        else:
            push_notification_translation_form = PushNotificationTranslationForm(request.POST)

        # If both forms are valid, save them
        if push_notification_form.is_valid() and push_notification_translation_form.is_valid():
            if push_notification:
                push_notification = push_notification_form.save()
            else:
                # The push notification cannot be created directly, because it has a required foreign key to region
                # (which has to be set indirectly before saving)
                push_notification = push_notification_form.save(commit=False)
                push_notification.region = region
                push_notification.save()
            if push_notification_translation:
                push_notification_translation_form.save()
            else:
                # The push notification translation cannot be created directly,
                # because it has a required foreign key to push notifications and languages
                # (which has to be set indirectly before saving)
                push_notification_translation = push_notification_translation_form.save(commit=False)
                push_notification_translation.push_notification = push_notification
                push_notification_translation.language = language
                push_notification_translation.save()
            messages.success(request, success_message)

            # Check if Save button has been clicked
            if push_notification_form.data.get('submit_send'):

                push_sent = self.push_sender.send(region.slug, push_notification.channel, push_notification_translation.title,
                                                  push_notification_translation.text, language.code)

                if push_sent:
                    push_notification.sent_date = timezone.now()
                    push_notification.save()
                    messages.success(request, _('Push notification was successfully sent.'))
                else:
                    messages.error(request, _('Error occurred sending the push notification'))

        else:
            messages.error(request, _('Errors have occurred.'))

        return render(request, self.template_name, {
            **self.base_context,
            'push_notification': push_notification,
            'push_notification_form': push_notification_form,
            'push_notification_translation_form': push_notification_translation_form,
            'language': language,
            'languages': region.languages,
        })
