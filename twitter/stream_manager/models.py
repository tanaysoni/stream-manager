from django.db import models

class Twitter_User(models.Model):
    twitter_id = models.CharField(max_length=20, unique=True, null=False, blank=False)
    name = models.CharField(max_length=60)
    followers_count = models.IntegerField(null=True, blank=True)


class Tweet(models.Model):
    retweet_count = models.PositiveIntegerField(default=0, null=True, blank=True)
    text = models.TextField()
    language = models.CharField(max_length=2, null=True, blank=True)
    tweet_by = models.ForeignKey(Twitter_User, related_name='tweet_by_user')