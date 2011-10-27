from plone.memoize.request import memoize_diy_request
from plone.memoize.view import memoize
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout

from Acquisition import aq_inner
from Products.Five import BrowserView
from wildcard.notrackingsocial.interfaces import ISocialSettings

from zope.component import getUtility
from plone.registry.interfaces import IRegistry


def isSocialable(request, context, settings=None):
    if not settings:
        settings = _socialSettings(request)
    portal_type = getattr(context, 'portal_type', '')
    return portal_type in settings.enabled_types


@memoize_diy_request(arg=0)
def _socialSettings(request):
    registry = getUtility(IRegistry)
    return registry.forInterface(ISocialSettings)


@memoize_diy_request(arg=0)
def _socialEnabled(request, context):
    context = aq_inner(context)
    enabled = getattr(context, '_social_enabled', None)
    if enabled is None:
        # only fall back to acceptable types if
        # social buttons not explicitly set.
        return isSocialable(request, context)
    return enabled


class SocialUtils(BrowserView):
    @memoize
    def socialable(self):
        return isSocialable(self.request, self.context)

    def toggle(self):
        context = aq_inner(self.context)
        enabled = getattr(context, '_social_enabled', False)
        if enabled:
            context._social_enabled = False
        else:
            context._social_enabled = True
        self.request.response.redirect(self.context.absolute_url() + '/view')


class SocialControlPanelForm(RegistryEditForm):
    schema = ISocialSettings


SocialControlPanelView = layout.wrap_form(
    SocialControlPanelForm, ControlPanelFormWrapper)
SocialControlPanelView.label = u"Social settings"