import snscrape.base
import snscrape.modules.twitter
import bs4

class TweetIdScraper(snscrape.base.Scraper):

    def __init__(self, tweetID = None, **kwargs):
        if tweetID is not None and tweetID.strip('0123456789') != '':
            raise ValueError('Invalid tweet ID, must be numeric')
        super().__init__(**kwargs)
        self._tweetID = tweetID

    def get_item(self):
        headers = {'User-Agent': f'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18 Bot'}

        r = self._get(f'https://twitter.com/user/status/{self._tweetID}', headers = headers)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        return soup