from django.conf.urls import url, include
from joke_bot.views import JokeBotView

urlpatterns = [
    url(r'^webhook/?$', JokeBotView.as_view())
]
