#import code; code.interact(local=dict(globals(), **locals()))
from django.shortcuts import render
from vanilla import TemplateView
from django.http.response import HttpResponse
# import os
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
import json, requests, re, random
from pprint import pprint

page_access_token = 'EAARggg3KkPYBACOwcqxdWAHFWZCCsIjxdgKuq0vKsRfBEh6YTkDiP8f6ZC710iPOgvwkhKW9VnK9WDtZCablXhRzgzilmvVBSSJnZB7LOBqDt9j43j9fRYXur6yKlZB1AaHOOnBMa5oyzGgKtRjDlmvPPbRiy8rA8smQ1KQHqhAZDZD'
proverbs = {
    'fingures': [
        'Agar ghee sidhi ungli se nahi niklta, to ungli tedhi karni padti hai!',
        'Ungli dene par hath pakad lena!',
        'Kai logo ko bat bat me ungli karne ki adat hoti hai!'
    ],
    'head': [
        'bina sir pair ki bat karna',
        'sir ghum jaana!',
        'use your head!'
    ]
}

cars = {
    'fabia': [
        'Petrol - 1.2l, gives mileage of 16-19 kmpl, very silent. Starts at 5.5L INR!',
        'Deisel - 1.2l Turbo charged engine, gives mileage of 22-23 kmpl, very powerful and long running. Starts at 6.5L INR!'
    ],
    'rapid': [
        'Petrol - 1.4l, gives mileage of 14-16 kmpl, very silent. Starts at 7.5L INR!',
        'Deisel - 1.6l Turbo charged engine, gives mileage of 20-23 kmpl, very powerful and long running. Starts at 9.5L INR!'
    ],
    'yeti':[
        'Petrol - 1.8l, gives mileage of 8-10 kmpl, very silent. Starts at 10L INR!',
        'Deisel - 1.9l Turbo charged engine, gives mileage of 15-18 kmpl, very powerful and long running. Starts at 13L INR!'
    ]
}

class JokeBotView(TemplateView):

    def __validate_request(self):
        if(self.request.GET.get('hub.mode') == 'subscribe' and self.request.GET.get('hub.verify_token') == '123456'):
            print("Validating webhook")
            return HttpResponse(self.request.GET.get('hub.challenge'))
        else:
            print("Failed validation. Make sure the validation tokens match.")
            return HttpResponse("", status=403)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.__validate_request()

    def post(self, request, *args, **kwargs):
        incoming_messages = json.loads(request.body.decode('utf-8'))
        print('===============================')
        pprint(incoming_messages)
        print('===============================')
        try:
            if incoming_messages['entry'][0]['messaging']:
                if 'message' in incoming_messages['entry'][0]['messaging'][0]:
                    pprint(incoming_messages['entry'][0]['messaging'][0])
                    if 'text' in incoming_messages['entry'][0]['messaging'][0]['message']:
                        post_facebook_message(incoming_messages['entry'][0]['messaging'][0]['sender']['id'], incoming_messages['entry'][0]['messaging'][0]['message']['text'])
                    else:
                        print("Seems non-text message! Can't send back!")
        except:
            pass
        try:
            if incoming_messages['entry'][0]['changes']:
                message = incoming_messages['entry'][0]['changes'][0]['value']['message']
                print('before===========')
                broadcast_message(message)
                print('after===========')
        except Exception as e:
            print(e)
        return HttpResponse(status=200)


def post_facebook_message(fbid, received_msg):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',received_msg).lower().split()
    text = ''
    try:
        user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
        user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':page_access_token}
        user_details = requests.get(user_details_url, user_details_params).json()
        pprint(user_details)
        joke_text = 'Yo '+user_details['first_name']
        user,is_created = Users.objects.get_or_create(sender_id = fbid, name = user_details['first_name']+' '+user_details['last_name'])
        # import code; code.interact(local=dict(globals(), **locals()))
        if is_created:    
            joke_text = 'hello '+user_details['first_name']+' please enter your details in following manner: 1. your mail-id 2. your num and we will get back to you with solution.'
    except Exception as e:
        print(e)
        joke_text = 'User'
    pprint(joke_text)
    for token in tokens:
        if token in proverbs:
            text = random.choice(proverbs[token])
            break
        if token in cars:
            text = "\n".join(map(str, cars[token]))
            break
    if not text:
        text = "I didn't get it, please send 'fingures', 'head' for a relevent proverb OR ask about Skoda cars by sending 'fabia', 'rapid', 'yeti'! "

    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

def broadcast_message(message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    sender_ids = Users.objects.values_list('sender_id')
    for sender_id in sender_ids:
        response_msg = json.dumps({"recipient": {"id": sender_id[0]}, "message": {"text": message}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        pprint(status.json())