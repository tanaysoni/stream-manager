from django.views.generic.base import TemplateView
from TwitterAPI import TwitterAPI
from .models import Tweet, Twitter_User
from django.db.models import Count
import time
from multiprocessing import Pool


def twitter_stream(hashtag):
    api = TwitterAPI(consumer_key='3bjVXQWtsIcNeaN8qs8UviHkM',
                     consumer_secret='n9izxhzxkypMOupCHN3I2twsAy7ow3Zi99JAAzvY1lHD2rSs8N',
                     access_token_key='251644435-OHGJhWoJwWkyBwcwp1ScHANF0GRgv7uFHy9ogPgE',
                     access_token_secret='lHxR9dwfxaIT25GrQX7q9ar4UJJb5qfGIiJuk9dVf0m4H')
    r = api.request('statuses/filter', {'track': hashtag})
    timeout = time.time() + 60 * 3  # Streaming will be open for 3 minutes

    for item in r:
        if time.time() > timeout:
            return
        user_name = item.get('user').get('name').encode('ascii', 'ignore')  # ignore foreign unicode characters
        user_id = item.get('user').get('id')
        followers_count = item.get('user').get('followers_count')
        try:
            user, created = Twitter_User.objects.get_or_create(twitter_id=user_id)

            if created:
                user.name = user_name
                user.followers_count = followers_count
                user.save()
            retweet_count = item.get('retweet_count')
            text = item.get('text').encode('ascii', 'ignore')
            language = item.get('lang')
            Tweet.objects.get_or_create(tweet_by=user, text=text, language=language, retweet_count=retweet_count)
        except Exception as e:
            print(e)

class LiveStream(TemplateView):
    template_name = 'live_stream.html'
    FLAG = 0
    result = 'please wait.. streaming Twitter API'

    def get(self, request, *args, **kwargs):
        if self.FLAG == 0:
            pool = Pool(processes=1)
            hashtag = request.GET.get('hashtag')
            pool.apply_async(twitter_stream, args=(hashtag,))
            self.FLAG = 1

        try:
            users_sorted_by_tweets = Twitter_User.objects.annotate(num_of_tweets=Count('tweet_by_user')).order_by(
                '-num_of_tweets')
            self.result = 'crunched ' + str(Tweet.objects.all().count()) + ' tweets and ' + str(
                Twitter_User.objects.all().count()) + ' users. Most tweets were by user: ' + users_sorted_by_tweets[0].name
        except Exception as e:
            print(e)

        return self.render_to_response({'result': self.result})
