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

emoji_arr = [["\ud83d\ude04", "Smiling Face with Open Mouth and Smiling Eyes"], ["\ud83d\ude04", "Smiling Face with Open Mouth"], ["\ud83d\ude04", "Grinning Face"], ["\ud83d\ude04", "Smiling Face with Smiling Eyes"], ["\ud83d\ude04", "White Smiling Face"], ["\ud83d\ude04", "Winking Face"], ["\ud83d\ude04", "Smiling Face with Heart-Shaped Eyes"], ["\ud83d\ude04", "Face Throwing a Kiss"], ["\ud83d\ude04", "Kissing Face with Closed Eyes"], ["\ud83d\ude04", "Kissing Face"], ["\ud83d\ude04", "Kissing Face with Smiling Eyes"], ["\ud83d\ude04", "Face with Stuck-Out Tongue and Winking Eye"], ["\ud83d\ude04", "Face with Stuck-Out Tongue and Tightly-Closed Eyes"], ["\ud83d\ude04", "Face with Stuck-Out Tongue"], ["\ud83d\ude04", "Flushed Face"], ["\ud83d\ude04", "Grinning Face with Smiling Eyes"], ["\ud83d\ude04", "Pensive Face"], ["\ud83d\ude04", "Relieved Face"], ["\ud83d\ude04", "Unamused Face"], ["\ud83d\ude04", "Disappointed Face"], ["\ud83d\ude04", "Persevering Face"], ["\ud83d\ude04", "Crying Face"], ["\ud83d\ude04", "Face with Tears of Joy"], ["\ud83d\ude04", "Loudly Crying Face"], ["\ud83d\ude04", "Sleepy Face"], ["\ud83d\ude04", "Disappointed but Relieved Face"], ["\ud83d\ude04", "Face with Open Mouth and Cold Sweat"], ["\ud83d\ude04", "Smiling Face with Open Mouth and Cold Sweat"], ["\ud83d\ude04", "Face with Cold Sweat"], ["\ud83d\ude04", "Weary Face"], ["\ud83d\ude04", "Tired Face"], ["\ud83d\ude04", "Fearful Face"], ["\ud83d\ude04", "Face Screaming in Fear"], ["\ud83d\ude04", "Angry Face"], ["\ud83d\ude04", "Pouting Face"], ["\ud83d\ude04", "Face with Look of Triumph"], ["\ud83d\ude04", "Confounded Face"], ["\ud83d\ude04", "Smiling Face with Open Mouth and Tightly-Closed Eyes"], ["\ud83d\ude04", "Face Savouring Delicious Food"], ["\ud83d\ude04", "Face with Medical Mask"], ["\ud83d\ude04", "Smiling Face with Sunglasses"], ["\ud83d\ude04", "Sleeping Face"], ["\ud83d\ude04", "Dizzy Face"], ["\ud83d\ude04", "Astonished Face"], ["\ud83d\ude04", "House Building"], ["\ud83d\ude04", "House with Garden"], ["\ud83d\ude04", "School"], ["\ud83d\ude04", "Office Building"], ["\ud83d\ude04", "Japanese Post Office"], ["\ud83d\ude04", "Hospital"], ["\ud83d\ude04", "Bank"], ["\ud83d\ude04", "Convenience Store"], ["\ud83d\ude04", "Love Hotel"], ["\ud83d\ude04", "Hotel"], ["\ud83d\ude04", "Wedding"], ["\ud83d\ude04", "Church"], ["\ud83d\ude04", "Department Store"], ["\ud83d\ude04", "European Post Office"], ["\ud83d\ude04", "Sunset over Buildings"], ["\ud83d\ude04", "Cityscape at Dusk"], ["\ud83d\ude04", "Japanese Castle"], ["\ud83d\ude04", "European Castle"], ["\ud83d\ude04", "Tent"], ["\ud83d\ude04", "Factory"], ["\ud83d\ude04", "Tokyo Tower"], ["\ud83d\ude04", "Silhouette of Japan"], ["\ud83d\ude04", "Mount Fuji"], ["\ud83d\ude04", "Sunrise over Mountains"], ["\ud83d\ude04", "Sunrise"], ["\ud83d\ude04", "Night with Stars"], ["\ud83d\ude04", "Statue of Liberty"], ["\ud83d\ude04", "Bridge at Night"], ["\ud83d\ude04", "Carousel Horse"], ["\ud83d\ude04", "Ferris Wheel"], ["\ud83d\ude04", "Fountain"], ["\ud83d\ude04", "Roller Coaster"], ["\ud83d\ude04", "Ship"], ["\ud83d\ude04", "Sailboat"], ["\ud83d\ude04", "Speedboat"], ["\ud83d\ude04", "Rowboat"], ["\ud83d\ude04", "Anchor"], ["\ud83d\ude04", "Rocket"], ["\ud83d\ude04", "Airplane"], ["\ud83d\ude04", "Seat"], ["\ud83d\ude04", "Helicopter"], ["\ud83d\ude04", "Steam Locomotive"], ["\ud83d\ude04", "Tram"], ["\ud83d\ude04", "Station"], ["\ud83d\ude04", "Dog Face"], ["\ud83d\ude04", "Wolf Face"], ["\ud83d\ude04", "Cat Face"], ["\ud83d\ude04", "Mouse Face"], ["\ud83d\ude04", "Hamster Face"], ["\ud83d\ude04", "Rabbit Face"], ["\ud83d\ude04", "Frog Face"], ["\ud83d\ude04", "Tiger Face"], ["\ud83d\ude04", "Koala"], ["\ud83d\ude04", "Bear Face"], ["\ud83d\ude04", "Pig Face"], ["\ud83d\ude04", "Pig Nose"], ["\ud83d\ude04", "Cow Face"], ["\ud83d\ude04", "Boar"], ["\ud83d\ude04", "Monkey Face"], ["\ud83d\ude04", "Monkey"], ["\ud83d\ude04", "Horse Face"], ["\ud83d\ude04", "Sheep"], ["\ud83d\ude04", "Elephant"], ["\ud83d\ude04", "Panda Face"], ["\ud83d\ude04", "Penguin"], ["\ud83d\ude04", "Bird"], ["\ud83d\ude04", "Baby Chick"], ["\ud83d\ude04", "Front-Facing Baby Chick"], ["\ud83d\ude04", "Hatching Chick"], ["\ud83d\ude04", "Chicken"], ["\ud83d\ude04", "Snake"], ["\ud83d\ude04", "Turtle"], ["\ud83d\ude04", "Bug"], ["\ud83d\ude04", "Honeybee"], ["\ud83d\ude04", "Ant"], ["\ud83d\ude04", "Lady Beetle"], ["\ud83d\ude04", "Snail"], ["\ud83d\ude04", "Octopus"], ["\ud83d\ude04", "Spiral Shell"], ["\ud83d\ude04", "Tropical Fish"], ["\ud83d\ude04", "Fish"], ["\ud83d\ude04", "Dolphin"], ["\ud83d\ude04", "Spouting Whale"], ["\ud83d\ude04", "Whale"], ["\ud83d\ude04", "Cow"], ["\ud83d\ude04", "Ram"], ["\ud83d\ude04", "Rat"], ["\ud83d\ude04", "Water Buffalo"], ["\ud83d\ude04", "Pine Decoration"], ["\ud83d\ude04", "Heart with Ribbon"], ["\ud83d\ude04", "Japanese Dolls"], ["\ud83d\ude04", "School Satchel"], ["\ud83d\ude04", "Graduation Cap"], ["\ud83d\ude04", "Carp Streamer"], ["\ud83d\ude04", "Fireworks"], ["\ud83d\ude04", "Firework Sparkler"], ["\ud83d\ude04", "Wind Chime"], ["\ud83d\ude04", "Moon Viewing Ceremony"], ["\ud83d\ude04", "Jack-o-lantern"], ["\ud83d\ude04", "Ghost"], ["\ud83d\ude04", "Father Christmas"], ["\ud83d\ude04", "Christmas Tree"], ["\ud83d\ude04", "Wrapped Present"], ["\ud83d\ude04", "Tanabata Tree"], ["\ud83d\ude04", "Party Popper"], ["\ud83d\ude04", "Confetti Ball"], ["\ud83d\ude04", "Balloon"], ["\ud83d\ude04", "Crossed Flags"], ["\ud83d\ude04", "Crystal Ball"], ["\ud83d\ude04", "Movie Camera"], ["\ud83d\ude04", "Camera"], ["\ud83d\ude04", "Video Camera"], ["\ud83d\ude04", "Videocassette"], ["\ud83d\ude04", "Optical Disc"], ["\ud83d\ude04", "DVD"], ["\ud83d\ude04", "Minidisc"], ["\ud83d\ude04", "Floppy Disk"], ["\ud83d\ude04", "Personal Computer"], ["\ud83d\ude04", "Mobile Phone"], ["\ud83d\ude04", "Black Telephone"], ["\ud83d\ude04", "Telephone Receiver"], ["\ud83d\ude04", "Pager"], ["\ud83d\ude04", "Fax Machine"], ["\ud83d\ude04", "Satellite Antenna"], ["\ud83d\ude04", "Television"], ["\ud83d\ude04", "Radio"], ["\ud83d\ude04", "Speaker with Three Sound Waves"], ["\ud83d\ude04", "Speaker with One Sound Wave"], ["\ud83d\ude04", "Speaker"], ["\ud83d\ude04", "Speaker with Cancellation Stroke"], ["\ud83d\ude04", "Bell"], ["\ud83d\ude04", "Bell with Cancellation Stroke"], ["\ud83d\ude04", "Keycap 1"], ["\ud83d\ude04", "Keycap 2"], ["\ud83d\ude04", "Keycap 3"], ["\ud83d\ude04", "Keycap 4"], ["\ud83d\ude04", "Keycap 5"], ["\ud83d\ude04", "Keycap 6"], ["\ud83d\ude04", "Keycap 7"], ["\ud83d\ude04", "Keycap 8"], ["\ud83d\ude04", "Keycap 9"], ["\ud83d\ude04", "Keycap 0"], ["\ud83d\ude04", "Keycap Ten"], ["\ud83d\ude04", "Input Symbol for Numbers"], ["\ud83d\ude04", "Hash Key"], ["\ud83d\ude04", "Input Symbol for Symbols"], ["\ud83d\ude04", "Upwards Black Arrow"], ["\ud83d\ude04", "Downwards Black Arrow"], ["\ud83d\ude04", "Leftwards Black Arrow"], ["\ud83d\ude04", "Black Rightwards Arrow"], ["\ud83d\ude04", "Input Symbol for Latin Capital Letters"], ["\ud83d\ude04", "Input Symbol for Latin Small Letters"], ["\ud83d\ude04", "Input Symbol for Latin Letters"], ["\ud83d\ude04", "North East Arrow"], ["\ud83d\ude04", "North West Arrow"], ["\ud83d\ude04", "South East Arrow"], ["\ud83d\ude04", "South West Arrow"], ["\ud83d\ude04", "Left Right Arrow"], ["\ud83d\ude04", "Up Down Arrow"], ["\ud83d\ude04", "Anticlockwise Downwards and Upwards Open Circle Arrows"], ["\ud83d\ude04", "Black Left-Pointing Triangle"], ["\ud83d\ude04", "Black Right-Pointing Triangle"], ["\ud83d\ude04", "Up-Pointing Small Red Triangle"], ["\ud83d\ude04", "Down-Pointing Small Red Triangle"], ["\ud83d\ude04", "Leftwards Arrow with Hook"], ["\ud83d\ude04", "Rightwards Arrow with Hook"], ["\ud83d\ude04", "Information Source"], ["\ud83d\ude04", "Black Left-Pointing Double Triangle"], ["\ud83d\ude04", "Black Right-Pointing Double Triangle"], ["\ud83d\ude04", "Black Up-Pointing Double Triangle"], ["\ud83d\ude04", "Black Down-Pointing Double Triangle"], ["\ud83d\ude04", "Arrow Pointing Rightwards Then Curving Downwards "], ["\ud83d\ude04", "Arrow Pointing Rightwards Then Curving Upwards"], ["\ud83d\ude04", "Squared OK"], ["\ud83d\ude04", "Twisted Rightwards Arrows"], ["\ud83d\ude04", "Clockwise Rightwards and Leftwards Open Circle Arrows"], ["\ud83d\ude04", "Thermometer"], ["\ud83d\ude04", "Black Droplet"], ["\ud83d\ude04", "White Sun"], ["\ud83d\ude04", "White Sun with Small Cloud"], ["\ud83d\ude04", "White Sun Behind Cloud"], ["\ud83d\ude04", "White Sun Behind Cloud with Rain"], ["\ud83d\ude04", "Cloud with Rain"], ["\ud83d\ude04", "Cloud with Snow"], ["\ud83d\ude04", "Cloud with Lightning"], ["\ud83d\ude04", "Cloud with Tornado"], ["\ud83d\ude04", "Fog"], ["\ud83d\ude04", "Wind Blowing Face"], ["\ud83d\ude04", "Hot Pepper"], ["\ud83d\ude04", "Fork and Knife with Plate"], ["\ud83d\ude04", "Heart with Tip on The Left"], ["\ud83d\ude04", "Bouquet of Flowers"], ["\ud83d\ude04", "Military Medal"], ["\ud83d\ude04", "Reminder Ribbon"], ["\ud83d\ude04", "Musical Keyboard with Jacks"], ["\ud83d\ude04", "Studio Microphone"], ["\ud83d\ude04", "Level Slider"], ["\ud83d\ude04", "Control Knobs"], ["\ud83d\ude04", "Beamed Ascending Musical Notes"], ["\ud83d\ude04", "Beamed Descending Musical Notes"], ["\ud83d\ude04", "Film Frames"], ["\ud83d\ude04", "Admission Tickets"], ["\ud83d\ude04", "Sports Medal"], ["\ud83d\ude04", "Weight Lifter"], ["\ud83d\ude04", "Golfer"], ["\ud83d\ude04", "Racing Motorcycle"], ["\ud83d\ude04", "Racing Car"], ["\ud83d\ude04", "Snow Capped Mountain"], ["\ud83d\ude04", "Camping"], ["\ud83d\ude04", "Beach with Umbrella"], ["\ud83d\ude04", "Building Construction"], ["\ud83d\ude04", "House Buildings"], ["\ud83d\ude04", "Cityscape"], ["\ud83d\ude04", "Derelict House Building"], ["\ud83d\ude04", "Classical Building"], ["\ud83d\ude04", "Desert"], ["\ud83d\ude04", "Desert Island"], ["\ud83d\ude04", "National Park"], ["\ud83d\ude04", "Stadium"], ["\ud83d\ude04", "White Pennant"], ["\ud83d\ude04", "White White Up Pointing Index"], ["\ud83d\ude04", "Light Brown White Up Pointing Index"], ["\ud83d\ude04", "Olive Toned White Up Pointing Index"], ["\ud83d\ude04", "Deeper Brown White Up Pointing Index"], ["\ud83d\ude04", "Black White Up Pointing Index"], ["\ud83d\ude04", "White Raised Fist"], ["\ud83d\ude04", "Light Brown Raised Fist"], ["\ud83d\ude04", "Olive Toned Raised Fist"], ["\ud83d\ude04", "Deeper Brown Raised Fist"], ["\ud83d\ude04", "Black Raised Fist"], ["\ud83d\ude04", "White Raised Hand"], ["\ud83d\ude04", "Light Brown Raised Hand"], ["\ud83d\ude04", "Olive Toned Raised Hand"], ["\ud83d\ude04", "Deeper Brown Raised Hand"], ["\ud83d\ude04", "Black Raised Hand"], ["\ud83d\ude04", "White Victory Hand"], ["\ud83d\ude04", "Light Brown Victory Hand"], ["\ud83d\ude04", "Olive Toned Victory Hand"], ["\ud83d\ude04", "Deeper Brown Victory Hand"], ["\ud83d\ude04", "Black Victory Hand"], ["\ud83d\ude04", "White Father Christmas"], ["\ud83d\ude04", "Light Brown Father Christmas"], ["\ud83d\ude04", "Olive Toned Father Christmas"], ["\ud83d\ude04", "Deeper Brown Father Christmas"], ["\ud83d\ude04", "Black Father Christmas"], ["\ud83d\ude04", "White Runner"], ["\ud83d\ude04", "Light Brown Runner"], ["\ud83d\ude04", "Olive Toned Runner"], ["\ud83d\ude04", "Deeper Brown Runner"], ["\ud83d\ude04", "Black Runner"], ["\ud83d\ude04", "White Surfer"], ["\ud83d\ude04", "Light Brown Surfer"], ["\ud83d\ude04", "Olive Toned Surfer"], ["\ud83d\ude04", "Deeper Brown Surfer"], ["\ud83d\ude04", "Black Surfer"], ["\ud83d\ude04", "White Horse Racing"], ["\ud83d\ude04", "Light Brown Horse Racing"], ["\ud83d\ude04", "Olive Toned Horse Racing"], ["\ud83d\ude04", "Deeper Brown Horse Racing"], ["\ud83d\ude04", "Black Horse Racing"], ["\ud83d\ude04", "White Swimmer"], ["\ud83d\ude04", "Light Brown Swimmer"], ["\ud83d\ude04", "Olive Toned Swimmer"], ["\ud83d\ude04", "Deeper Brown Swimmer"]]

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

    message_object3 = {
        "message":{
            "attachment":{
                "type":"image",
                "payload":{
                    "url":"http://worldversus.com/img/ironman.jpg"
                }
            }
        }
    }

    message_object2 = {
        "text": joke_text
        }
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    response_msg2 = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
    
    response_msg3 = json.dumps(
        {"recipient":{"id":fbid}, 
            "message":{
                "attachment":{
                    "type":"image",
                    "payload":{
                        "url":"http://worldversus.com/img/ironman.jpg"
                    }
                }
            }
     })
    
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg3)
    
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



