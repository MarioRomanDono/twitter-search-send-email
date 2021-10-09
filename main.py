from twitter_search import twitter_search
from send_email import send_email

search_result = twitter_search()
send_email(search_result)