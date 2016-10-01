    #!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

PAGE_ACCESS_TOKEN = 'EAAZAg3eueoxUBAAdTsps670ekn6haHMS7kH0RVZBCsztWhkjuZBYJ60jQ318lv0PAXJHagBN6CHrhOWWf3pMHrC6p7LI7jnHAIAVY6P26BfX5d6JIp5oZC7tAmJLBnP9bQ6DxnujWu0Gr15Xvnq8vFT2mZBmgJwaHJRleH6nNWQZDZD'
VERIFY_TOKEN = '8447789934m'

def logg(mess,meta='log',symbol='#'):
  print '%s\n%s\n%s'%(symbol*20,mess,symbol*20)


def set_greeting_text():
    post_message_url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s"%PAGE_ACCESS_TOKEN
    greeting_text = "Hello and welcome to my bot"
    greeting_object = json.dumps({"setting_type":"greeting", "greeting":{"text":greeting_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=greeting_object)
    pprint(status.json())

def index(request):
    #set_greeting_text()
    post_facebook_message('100006427286608','mango')
    return HttpResponse('Hello World',content_type='application/json')

def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    recevied_message = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower()
    
    response_text = recevied_message
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

class BotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        incoming_message= json.loads(self.request.body.decode('utf-8'))
        
        logg(incoming_message)

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                
                try:
                    sender_id = message['sender']['id']
                    message_text = message['message']['text']
                    post_facebook_message(sender_id,message_text) 
                except Exception as e:
                    logg(e,symbol='-332-')

        return HttpResponse()  



