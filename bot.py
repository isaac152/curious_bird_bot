
import telebot
from telebot import types
import random
from bird_dictionary import Bird_bot
import json

TOKEN='<api_token>'
bot= telebot.TeleBot(TOKEN,parse_mode='HTML')

def load_file(name):
    filename= f'./json/{name}.json'
    with open(filename,'r') as json_data:
        j=json_data.read()
    return json.loads(j)
#change here for the file you want.
list_json=load_file('name')
birds_list=[Bird_bot(**i) for i in list_json]

def random_bird_picker(bird_list):
    return bird_list[random.randint(0,len(bird_list)-1)]

def random_audio_picker(bird_list):
    birds=[]
    while(len(birds)<4):
        bird=random_bird_picker(bird_list)
        if(bird.audio!=None):
            birds.append(bird)
    return birds

class Game():
    score=0
    answer=''
    round=1
    playing=''
    funct=''

    def win_game(self,bird,option):
        return True if option==bird else False

    def msg_game(self,msg):
        try:
            if(self.win_game(self.answer,msg.text)):
                bot.send_message(msg.chat.id,'Nice one \U0001F601')
                self.score+=1
                self.round+=1
                self.funct=getattr(self,self.playing)
                self.funct(msg)
            else:
                bot.send_message(msg.chat.id,'Wrong answer, sorry \U0001F614')
                bot.send_message(msg.chat.id,f'The answer was {self.answer}')
                bot.send_message(msg.chat.id,f'Your score was: {self.score}')
        except Exception as e:
            bot.send_message(msg,'Sorry, something happened \U0001F625')
            print(e)
            print('exception in wining')

    def guessbyimage(self,msg):
        self.funct=''
        try:
            bot.send_message(msg.chat.id,f'Round {self.round}')
            birds=[random_bird_picker(birds_list) for i in range(0,4)]
            bird=random_bird_picker(birds)
            self.answer=bird.common_name
            print('https://ebird.org/species/'+bird.code)
            print(self.answer)
            markup= types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True,selective=True)
            for b in birds:
                markup.add(b.common_name)
            bot.send_message(msg.chat.id,'Wait please, the image is loading \U0001F62C')
            bot.send_photo(msg.chat.id,bird.get_image())
            m=bot.send_message(msg.chat.id,'Guess the bird',reply_markup=markup)
            bot.register_next_step_handler(m,self.msg_game)
        except Exception as e:
            print(e)
            print('exception in image')
            bot.send_message(msg,'Sorry, something happened \U0001F625')
    def guessbysound(self,msg):
        self.funct=''
        try:
            bot.send_message(msg.chat.id,f'Round {self.round}')
            birds=random_audio_picker(birds_list)
            bird=random_bird_picker(birds)
            self.answer=bird.common_name
            print(self.answer)
            print('https://ebird.org/species/'+bird.code)
            markup= types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True,selective=True)
            for b in birds:
                markup.add(b.common_name)
            bot.send_message(msg.chat.id,'Wait please,the sound is loading \U0001F62C')
            bot.send_audio(msg.chat.id,bird.get_audio(),title=f'Audio {self.round}')
            m=bot.send_message(msg.chat.id,'Guess the bird',reply_markup=markup)
            bot.register_next_step_handler(m,self.msg_game)
        except Exception as e:
            print(e)
            print('exception in sound')
            bot.send_message(msg,'Sorry, something happened \U0001F625')


def send_html(bird,bot,id):
    description=bird.description
    if(description==None):
        description='Not available \U0001F615'
    bot.send_message(id,f'<b>Scientific Name: </b> {bird.scientific_name}')
    bot.send_message(id,f'<b>Common Name: </b> {bird.common_name}')
    bot.send_message(id,f'<b>Description: </b> {description}')
    bot.send_message(id,f'Learn more about this awesome bird, <a href="{bird.url}">here</a>')
    

#TELEGRAM FUNCTIONS

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message, "So you like birds? Me too!")
    bot.send_message(message.chat.id,'You can interact with me by the following commands: ')
    bot.send_message(message.chat.id,'/game -> Guess the bird by sound or photo, is really fun, you should try it ')
    bot.send_message(message.chat.id,'/surpriseme -> I will send you a random bird with their description, photo and audio')
    bot.send_message(message.chat.id,'/about -> Copyright about the content')
    bot.send_message(message.chat.id,'I hope we can learn a lot together.')




@bot.message_handler(commands=['about'])
def about(message):
    chat=message.chat.id
    bot.send_message(chat,'All data was extracted from ebird.')
    bot.send_message(chat,'If you wanna learn more about birds, visit their website')
    bot.send_message(chat,'Every contributor (photo or audio) retains full copyright about the material')
    bot.send_message(chat,'This bot does not have any commercial or monetary purpose')
    bot.send_message(chat,'Made by: Isaac152, a bird lover')
    bot.send_message(chat,'Long live the birds \U0001F989 \U0001F427 \U0001F986')


@bot.message_handler(commands=['surpriseme'])
def random_bird(message):
    bird=random_bird_picker(birds_list)
    bot.send_message(message.chat.id,'Wait please \U0001F62C')
    bot.send_photo(message.chat.id,bird.get_image())
    if(bird.audio!=None):
        bot.send_audio(message.chat.id,bird.get_audio(),title=bird.common_name)
    else:
        bot.send_message(message.chat.id,'This bird has not been recorded yet. Crazy, huh? \U0001F612 ')
    send_html(bird,bot,message.chat.id)

@bot.message_handler(commands=['game'])
def game_menu(message):
    markup= types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
    choice1=types.KeyboardButton('Guess by sound')
    choice2=types.KeyboardButton('Guess by image')
    markup.add(choice1,choice2)
    msg=bot.reply_to(message,'Which game do you want to play?',reply_markup=markup)
    try:
        bot.register_next_step_handler(msg,choicefunction)
    except:
        bot.reply_to(message,'sorry an error has ocurred')

def choicefunction(msg):
    game=Game()
    game.playing=msg.text.replace(' ','').lower()
    try:
        if(msg.text=='Guess by sound'):
            game.guessbysound(msg)
        else:
            game.guessbyimage(msg)
    except:
        bot.reply_to(msg,'sorry an error has ocurred')
    
    
bot.polling()
