import datetime
import random
import os
import spotipy
from json.decoder import JSONDecodeError


class Spotipy():
    def authorize(self):
        spotify_username = os.environ.get('spotify_username')
        scope = 'user-read-private user-read-playback-state user-modify-playback-state'
        Spotify_Client_ID = os.environ.get('Spotify_Client_ID')
        Spotify_Client_Secret = os.environ.get('Spotify_Client_Secret')
        spotifyObject = None

        try:
            auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=Spotify_Client_ID,
                                                       client_secret=Spotify_Client_Secret,
                                                       redirect_uri='https://www.spotify.com/', scope=scope)
            spotifyObject = spotipy.Spotify(auth_manager=auth_manager)
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{spotify_username}")
            auth_manager = spotipy.oauth2.SpotifyOAuth(client_id='60a4caba232a48b9a33a994cbf4864e6',
                                                       client_secret='131b5a011b3b43e0a24240c37b3e234d',
                                                       redirect_uri='https://www.spotify.com/', scope=scope)
            spotifyObject = spotipy.Spotify(auth_manager=auth_manager)
        return spotifyObject


    def get_song(self):
        devices = spotifyObject.devices()
        deviceID = devices['devices'][0]['id']

        while True:

            print("1 - Wake up to song of your choice")
            print("2 - Wake up to default alarm sound")
            choice = input("Enter your choice: ")

            while choice != "1" and choice != '2':
                choice = input('Invalid Entry, press 1 to choose song or press 2 for default alarm sound ')

            def choosing_song(artist, song_selection, choice):
                track_list = spotifyObject.search(q="artist:" + artist + " track:" + song_selection, type="track")
                track_list = track_list['tracks']['items']

                z = 0
                trackURIs = []
                for item in track_list:
                    print(str(z) + ": " + item['name'])
                    trackURIs.append(item['uri'])
                    z += 1


                trackSelectionList = []
                if choice == "1":
                    songNum = AlarmClock()
                    print('Enter a song number to wake up to: ')
                    song_num_phrase = 'Enter Enter song number Between 0 and {}'.format(z-1)
                    songSelection = songNum.check_for_int_input(song_num_phrase)
                    while songSelection < 0 or songSelection > z:
                        print('Invalid song number. Enter song number Between 0 and {}'.format(z-1))
                        songSelection = songNum.check_for_int_input(song_num_phrase)
                    trackSelectionList.append(trackURIs[songSelection])
                elif choice == "2":
                    trackSelectionList.append(trackURIs[0])
                return [deviceID, trackSelectionList]

            if choice == "1":
                print()
                artist = input('Enter artist name: ')
                song_selection = input("Enter song name: ")
                print()
                return choosing_song(artist, song_selection, choice)

            elif choice == "2":
                return choosing_song("Sound Effect Nation", "Alarm Clock Radio Sound Effects", choice)


class AlarmClock():

    def inputs(self):
        time = self.set_alarmtime()
        alarm_time = time[0]
        day_period = time[1]

        print('How many questions do you want to wake up to? ')
        num_questions_phrase = 'Enter number of questions of at least 0'
        num_questions = self.check_for_int_input(num_questions_phrase)
        while num_questions < 0:
            print('Invalid Input. Enter number of questions of at least 0')
            num_questions = self.check_for_int_input(num_questions_phrase)

        spotipy = Spotipy()
        songs = spotipy.get_song()
        device_ID = songs[0]
        track_list = songs[1]
        return [alarm_time, num_questions, device_ID, track_list, day_period]


    def questions(self,num):
        questions_remaining = num
        while questions_remaining > 0:
            a = random.randint(0,10)
            b = random.randint(0,10)
            phrase = 'Answer must be a number. Try again {} + {}'.format(a,b)
            print('Solve {} + {} = '.format(a,b))
            answer = self.check_for_int_input(phrase)
            while answer != a + b:
                print('Wrong Try Again: {} + {} = '.format(a, b))
                answer = self.check_for_int_input(phrase)
            questions_remaining -= 1
            print('Correct...{} questions remaining'.format(questions_remaining))
        return True



    def set_alarmtime(self):
        print('Enter Hour of Alarm Time: ')
        hr_phrase = 'Enter Hour Between 1 and 12'
        hour = self.check_for_int_input(hr_phrase)
        while hour < 1 or hour > 12:
            print('Invalid Input. Enter Hour Between 1 and 12')
            hour = self.check_for_int_input(hr_phrase)

        print('Enter Minute of Alarm Time: ')
        min_phrase = 'Enter Minute Between 00 and 59'
        mins = self.check_for_int_input(min_phrase)
        while mins < 0 or mins > 59:
            print('Invalid Input. Enter Minute Between 00 and 59:')
            mins = self.check_for_int_input(min_phrase)
        day_period = input('AM or PM: ')

        while day_period.upper() != "AM" and day_period.upper() != "PM":
            day_period = input('Invalid Format. Enter AM or PM: ')
        if day_period.upper() == "PM" and hour < 12:
            hour = 12 + int(hour)

        alarmtime = datetime.datetime.now()
        alarmtime = alarmtime.replace(hour=hour, minute=mins)
        return [alarmtime, day_period]


    def wait_for_alarm(self, alarm_hr, alarm_min, device_ID, track_list):
        while True:
            current_hr, current_min = int(datetime.datetime.now().strftime("%I")),int(datetime.datetime.now().strftime("%M"))
            if current_hr == alarm_hr and current_min == alarm_min:
                break
        alarm_functionality.alarm_on(device_ID, track_list)


    def alarm_on(self, deviceID, trackSelectionList):
        spotifyObject.start_playback(deviceID, None, trackSelectionList)

    def alarm_off(self, deviceID):
        spotifyObject.pause_playback(deviceID)

    def check_for_int_input(self, phrase):
        while True:
            try:
                user_input = int(input(' '))
                break
            except ValueError:
                print('Invalid Input: {} '.format(phrase))
        return user_input


class Alarm():
    def __init__(self, alarmTime, num_questions, device_ID, track_list, day_period):
        self.alarmTime = alarmTime
        self.num_questions = num_questions
        self.device_ID = device_ID
        self.track_list = track_list
        self.day_period = day_period

alarm_functionality = AlarmClock()
spotify = Spotipy()
spotifyObject = spotify.authorize()
alarm_functionality_inputs = alarm_functionality.inputs()

alarm_individual = Alarm(alarm_functionality_inputs[0],alarm_functionality_inputs[1], alarm_functionality_inputs[2],alarm_functionality_inputs[3], alarm_functionality_inputs[4])
#alarm inputs
c = alarm_individual.alarmTime
alarm_hr, alarm_min = int(alarm_individual.alarmTime.strftime("%I")), int(alarm_individual.alarmTime.strftime("%M"))
num_questions = alarm_individual.num_questions
device_ID = alarm_individual.device_ID
track_list = alarm_individual.track_list

def display_time(alarm_hr, alarm_min):
    military_hr = int(alarm_individual.alarmTime.strftime("%H"))
    if alarm_min < 10:
        alarm_min_display = "0" + str(alarm_min)
    else:
        alarm_min_display = str(alarm_min)
    if military_hr > 12:
        alarm_hour_display = str(military_hr - 12)
        return "Alarm Set for {}:{} PM".format(alarm_hour_display,alarm_min_display)
    elif military_hr < 12:
        alarm_hour_display = str(alarm_hr)
        return"Alarm Set for {}:{} AM".format(alarm_hour_display, alarm_min_display)
    else:
        if alarm_individual.day_period.upper() == "AM":
            return "Alarm Set for {}:{} AM".format(military_hr, alarm_min_display)
        elif alarm_individual.day_period.upper() == "PM":
            return "Alarm Set for {}:{} PM".format(military_hr, alarm_min_display)
print(display_time(alarm_hr,alarm_min))
alarm_functionality.wait_for_alarm(alarm_hr, alarm_min, device_ID, track_list)

while True:
    snooze = input('Press 1 to snooze for 10 minutes, Press 2 to turn Alarm off ')
    while snooze != "1" and snooze != "2":
        snooze = input('Invalid Entry: Press 1 to snooze for 10 minutes, Press 2 to turn Alarm off ')
    if snooze == "1":
        alarm_functionality.alarm_off(device_ID)
        current_time = datetime.datetime.now()
        new_time = current_time + datetime.timedelta(minutes=10)
        new_hr,new_min = int(new_time.strftime("%I")), int(new_time.strftime("%M"))
        print(display_time(new_hr,new_min))
        alarm_functionality.wait_for_alarm(new_hr, new_min, device_ID, track_list)

    elif snooze == '2':
        if num_questions == 0:
            alarm_functionality.alarm_off(device_ID)
            quit()
        while num_questions > 0:
            if alarm_functionality.questions(num_questions):
                alarm_functionality.alarm_off(device_ID)
                quit()

