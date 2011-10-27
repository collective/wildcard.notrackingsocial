from plone.app.layout.viewlets.common import ViewletBase
from wildcard.notrackingsocial.browser.views import _socialSettings
from wildcard.notrackingsocial.browser.views import _socialEnabled


class SocialViewlet(ViewletBase):
    """
    social viewlet enabled for only file types that
    implement IAudioEnhanced or the page-turner view
    """

    def update(self):
        super(SocialViewlet, self).update()
        self.enabled = _socialEnabled(self.request, self.context)
        self.url = self.context.absolute_url()
        self.settings = _socialSettings(self.request)
        self.title = self.context.Title()

    def button_enabled(self, button):
        return button in self.settings.enabled_buttons

    def plus_url(self):
        return "https://m.google.com/app/plus/x/?hideloc=1&v=compose&" + \
               "content=%s - %s" % (self.title, self.url)

    def plus_on_click(self):
        return """window.open('https://m.google.com/app/plus/x/?hideloc=1&v=""" + \
               """compose&content=%s - %s',""" % (self.title, self.url) + \
               """'gplusshare','width=600,height=400');return false;"""


class SocialTopViewlet(SocialViewlet):

    def update(self):
        super(SocialTopViewlet, self).update()
        if self.enabled:
            self.enabled = self.settings.show_top


class SocialBottomViewlet(SocialViewlet):

    def update(self):
        super(SocialBottomViewlet, self).update()
        if self.enabled:
            self.enabled = self.settings.show_bottom


class SocialHead(SocialViewlet):
    def twitter_javascript(self):
        return """
jq(function(){
jq.ajax({
    url : 'http://urls.api.twitter.com/1/urls/count.json?url=%(url)s',
    dataType : 'jsonp',
    success : function(data){
        count = data['count'];
        if(count > 0){
            jq('li.twitter-share-button a span').
                html('(' + addCommas(count) + ')');
            jq('li.twitter-share-button a span').fadeIn();
        }
    }
});

});""" % {'url': self.url}

    def facebook_javascript(self):
        return """
window.fbAsyncInit = function() {
  jq(function(){
  FB.api({
      method: 'fql.query',
      query: 'SELECT total_count FROM link_stat ' +
             'WHERE url="%(url)s" ORDER BY total_count LIMIT 1;'
    },
    function(response) {
        try{
            var count = response[0].total_count;
            if(count !== undefined && count > 0){
                jq('li.facebook-share-button a span').
                    html(' (' + addCommas(response[0].total_count) + ')');
                jq('li.facebook-share-button a span').fadeIn();
            }
        }catch(e){}
    }
  );
  });
};""" % {'url': self.url}
