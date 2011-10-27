from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.interface import Interface
from zope.schema import Tuple
from zope.schema import Choice
from zope.schema import Bool


class ILayer(Interface):
    pass


class ISocialSettings(Interface):

    enabled_types = Tuple(
        title=u'Enabled Types',
        description=u"Select the types you would like"
            u'to have the social media buttons on automatically. '
            u'This does not prevent you from manually enabling '
            u'social buttons on individual pages.',
        required=False,
        default=('Document', 'News Item', 'Event'),
        value_type=Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes"
        )
    )

    enabled_buttons = Tuple(
        title=u'Enabled Buttons',
        description=u'The buttons that will show up',
        required=False,
        default=('twitter', 'facebook', 'share', 'print', 'mail'),
        value_type=Choice(
            vocabulary=SimpleVocabulary([
                SimpleTerm('twitter', 'twitter', u'Twitter'),
                SimpleTerm('facebook', 'facebook', u'Facebook'),
                SimpleTerm('plus', 'plus', u'Google+'),
                SimpleTerm('share', 'share', u'Share(Add This)'),
                SimpleTerm('print', 'print', u'Print'),
                SimpleTerm('mail', 'mail', u'Mail')
            ])
        )
    )

    show_top = Bool(
        title=u'Show Top Buttons',
        required=False,
        default=True
    )

    show_bottom = Bool(
        title=u'Show Bottom Buttons',
        required=False,
        default=True
    )
