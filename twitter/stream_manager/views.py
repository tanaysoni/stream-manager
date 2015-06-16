from django.views.generic.base import TemplateView
from django.http import HttpResponse
from TwitterAPI import *
from .models import Tweet, Twitter_User
from django.db.models import Count


class HomeView(TemplateView):
    template_name = 'stream_manager.html'

    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        api = TwitterAPI(consumer_key='3bjVXQWtsIcNeaN8qs8UviHkM',
                         consumer_secret='n9izxhzxkypMOupCHN3I2twsAy7ow3Zi99JAAzvY1lHD2rSs8N',
                         access_token_key='251644435-OHGJhWoJwWkyBwcwp1ScHANF0GRgv7uFHy9ogPgE',
                         access_token_secret='lHxR9dwfxaIT25GrQX7q9ar4UJJb5qfGIiJuk9dVf0m4H')

        NUM_OF_ITERATIONS = 2
        hashtag = '#' + request.POST.get('hashtag')
        while NUM_OF_ITERATIONS:
            r = api.request('search/tweets', {'q': hashtag})
            for item in r:
                user_name = item.get('user').get('name').encode('ascii', 'ignore')  # ignore foreign unicode characters
                user_id = item.get('user').get('id')
                followers_count = item.get('user').get('followers_count')
                user, created = Twitter_User.objects.get_or_create(twitter_id=user_id)
                if created:
                    user.name = user_name
                    user.followers_count = followers_count
                    user.save()
                retweet_count = item.get('retweet_count')
                text = item.get('text').encode('ascii', 'ignore')
                language = item.get('lang')
                Tweet.objects.get_or_create(tweet_by=user, text=text, language=language, retweet_count=retweet_count)

            NUM_OF_ITERATIONS -= 1

        users_sorted_by_tweets = Twitter_User.objects.annotate(num_of_tweets=Count('tweet_by_user')).order_by(
            '-num_of_tweets')
        result = 'crunched ' + str(Tweet.objects.all().count()) + ' tweets and ' + str(
            Twitter_User.objects.all().count()) + ' users. Most tweets were by user: ' + users_sorted_by_tweets[0].name
        return HttpResponse(result)
