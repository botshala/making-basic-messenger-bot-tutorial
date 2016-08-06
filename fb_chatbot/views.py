import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

PAGE_ACCESS_TOKEN = 'EAAYgQ8PcnXcBAMoZC2E1QWAem7VOc7VLvUsTNNHCNx2seOF5CFoMYkodiPk7jgW98ALPIkx8Q8h46joQh93A4EEIs5dmvQXvERRUIMKZCbbna73yGvvusB9tryP5B17TKXXgaajBTDVgZB8r1a4M2qAuaJ9NqkkuHA3ZCHDtZCQZDZD'
VERIFY_TOKEN = '8447789934m'

def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    #clean_message = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message)

    reply_text = ''
    

    if not reply_text:
        reply_text = recevied_message

    try:
        user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
        user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
        user_details = requests.get(user_details_url, user_details_params).json() 
        joke_text = 'Yo '+user_details['first_name']+'..! ' + reply_text
    except:
        joke_text = 'Yo ' + reply_text

    
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class MyQuoteBotView(generic.View):
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
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    try:
                        post_facebook_message(message['sender']['id'], message['message']['text'])    
                    except:
                        print 'Oops'
                        pass

        return HttpResponse()    



def index(request):
    test()
    return HttpResponse("Hello World")

def test():
    post_facebook_message('abhishek.sukumar.1', 'hello')


def hello(request):
    return HttpResponse('By Bye world')