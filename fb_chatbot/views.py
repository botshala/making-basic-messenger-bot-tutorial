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

PAGE_ACCESS_TOKEN = 'EAAYgQ8PcnXcBAMoZC2E1QWAem7VOc7VLvUsTNNHCNx2seOF5CFoMYkodiPk7jgW98ALPIkx8Q8h46joQh93A4EEIs5dmvQXvERRUIMKZCbbna73yGvvusB9tryP5B17TKXXgaajBTDVgZB8r1a4M2qAuaJ9NqkkuHA3ZCHDtZCQZDZD'
VERIFY_TOKEN = '8447789934m'

quotes_arr = [["Life isn’t about getting and having, it’s about giving and being.", "Kevin Kruse"],
["Whatever the mind of man can conceive and believe, it can achieve.", "Napoleon Hill"],
["Strive not to be a success, but rather to be of value.", "Albert Einstein"],
["Every strike brings me closer to the next home run.", "Babe Ruth"],
["Definiteness of purpose is the starting point of all achievement.", "W. Clement Stone"],
["We must balance conspicuous consumption with conscious capitalism.", "Kevin Kruse"],
["Life is what happens to you while you’re busy making other plans.", "John Lennon"],
["We become what we think about.", "Earl Nightingale"],
["14.Twenty years from now you will be more disappointed by the things that you didn’t do than by the ones you did do, so throw off the bowlines, sail away from safe harbor, catch the trade winds in your sails.  Explore, Dream, Discover.", "Mark Twain"],
["15.Life is 10% what happens to me and 90% of how I react to it.", "Charles Swindoll"],
["The most common way people give up their power is by thinking they don’t have any.", "Alice Walker"],
["The mind is everything. What you think you become.", "Buddha"],
["The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"],
["An unexamined life is not worth living.", "Socrates"],
["Every child is an artist.  The problem is how to remain an artist once he grows up.", "Pablo Picasso"],
["You can never cross the ocean until you have the courage to lose sight of the shore.", "Christopher Columbus"],
["I’ve learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.", "Maya Angelou"],
["Either you run the day, or the day runs you.", "Jim Rohn"],
["Whether you think you can or you think you can’t, you’re right.", "Henry Ford"],
["The two most important days in your life are the day you are born and the day you find out why.", "Mark Twain"],
["Whatever you can do, or dream you can, begin it.  Boldness has genius, power and magic in it.", "Johann Wolfgang von Goethe"],
["The best revenge is massive success.", "Frank Sinatra"],
["People often say that motivation doesn’t last. Well, neither does bathing.  That’s why we recommend it daily.", "Zig Ziglar"],
["Life shrinks or expands in proportion to one’s courage.", "Anais Nin"],
["If you hear a voice within you say “you cannot paint,” then by all means paint and that voice will be silenced.", "Vincent Van Gogh"],
["There is only one way to avoid criticism: do nothing, say nothing, and be nothing.", "Aristotle"],
["Ask and it will be given to you; search, and you will find; knock and the door will be opened for you.", "Jesus"],
["The only person you are destined to become is the person you decide to be.", "Ralph Waldo Emerson"],
["Go confidently in the direction of your dreams.  Live the life you have imagined.", "Henry David Thoreau"],
["When I stand before God at the end of my life, I would hope that I would not have a single bit of talent left and could say, I used everything you gave me.", "Erma Bombeck"],
["Few things can help an individual more than to place responsibility on him, and to let him know that you trust him.", "Booker T. Washington"],
["Certain things catch your eye, but pursue only those that capture the heart.", " Ancient Indian Proverb"],
["Believe you can and you’re halfway there.", "Theodore Roosevelt"],
["Everything you’ve ever wanted is on the other side of fear.", "George Addair"],
["We can easily forgive a child who is afraid of the dark; the real tragedy of life is when men are afraid of the light.", "Plato"],
["Teach thy tongue to say, “I do not know,” and thous shalt progress.", "Maimonides"],
["Start where you are. Use what you have.  Do what you can.", "Arthur Ashe"],
["When I was 5 years old, my mother always told me that happiness was the key to life.  When I went to school, they asked me what I wanted to be when I grew up.  I wrote down ‘happy’.  They told me I didn’t understand the assignment, and I told them they didn’t understand life.", "John Lennon"],
["Fall seven times and stand up eight.", "Japanese Proverb"],
]


def return_random_quote():
    random.shuffle(quotes_arr)
    return quotes_arr[0]

def quote_search(str_var):
    str_var.lower()
    random.shuffle(quotes_arr)
    for quote_text,quote_author in quotes_arr:
        if str_var in quote_author.lower():
            return quote_text

    return return_random_quote()[0]


def post_facebook_message(fbid, recevied_message):
    reply_text = recevied_message + ':)'

    try:
        user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
        user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
        user_details = requests.get(user_details_url, user_details_params).json() 
        joke_text = 'Yo '+user_details['first_name']+'..! ' + reply_text
    except:
        joke_text = 'Yo ' + reply_text

    joke_text = quote_search(recevied_message)
    response_text = recevied_message +' :)'

    message_object = {
        "attachment":{
          "type":"image",
          "payload":{
            #"url":"http://thecatapi.com/api/images/get?format=src&type=png"
            "url" : "http://worldversus.com/img/ironman.jpg"
          }
        }
    }

    message_object2 = {
        "text": joke_text
        }
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    response_msg2 = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
    
    response_msg3 = json.dumps({"recipient":{"id":fbid}, "message": message_object})
    
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    #status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg2)
    
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
                    post_facebook_message(message['sender']['id'], message['message']['text'])    
                    

        return HttpResponse()    



def index(request):
    print test()
    print quote_search('z123io90')
    return HttpResponse("Hello World" + quote_search('*'))

def test():
    post_facebook_message('abhishek.sukumar.1','test message')



