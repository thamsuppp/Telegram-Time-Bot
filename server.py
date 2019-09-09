#Import class from the other file
from bot import telegram_chatbot
import datetime
import random
import googlecalendar
from StudyTracker import StudyTracker
update_id = None

bot = telegram_chatbot('config.cfg')
study_tracker = StudyTracker()

def make_reply(msg):
    try:
        if msg is not None:
            #Splits message into list of items
            output = msg.split(', ')

            #Get the command (1st item in the comma-separated list)
            command = output[0]

            #Get the arguments (if any) (subsequent items in the comma-separated list)
            if len(output) > 1:
                args = output[1:]
            else:
                args = None

            print('Command is')
            print(command)
            print('Arguments are')
            print(args)

            #Returns help text
            if command == 'Help':
                help_text = '''
                Commands:
                Random - returns random integer from 1 to 10
                Calendar, getEvents, (n_days_ahead) - returns events in calendar (in the next n days)
                Calendar, addEvent, summary, start_time_str, duration - add event to calendar
                Start, Study, Subject, Task Name - starts logging a studying session (Go on airplane mode then send End)
                End - stops logging studying session
                Summary, Study - gives summary of study time
                '''
                return help_text

            #Random number generator from 1 to 10
            elif command == 'Random':
                reply = random.randint(1, 11)

            #Times the amount of time I actually study
            elif command == 'Start':
                if args[0] == 'Study':
                    #Start, Study, Subject, TaskName
                    reply = study_tracker.start_task(args[1], args[2])

                else:
                    reply = 'Error: Unknown argument after Start'

            #Ends the current study session
            elif command == 'End':
                reply = study_tracker.end_task()

            #Gives summary statistics of study session
            elif command == 'Summary':
                if args[0] == 'Study':
                    reply = study_tracker.get_summary()

            elif command == 'Calendar':
                #Returns calendar events
                if args[0] == 'getEvents':
                    if len(args) > 1:
                        reply = googlecalendar.get_calendar_events(n_days_ahead = int(args[1]))
                    else: 
                        reply = googlecalendar.get_calendar_events()

                #Adds calendar event
                elif args[0] == 'addEvent':
                    reply = googlecalendar.create_event(summary = args[1], start_time_str = args[2], duration = float(args[3]))
            else:
                reply = 'Okay'
            return reply
    except:
        return 'Error'
    
while True:
    print('...')
    updates = bot.get_updates(offset = update_id)
    updates = updates['result']

    if updates:
        #Item is a nested dictionary for each message
        for item in updates:
            update_id = item['update_id']
            try:
                message = str(item['message']['text'])
            except:
                message = None
            from_ = item['message']['from']['id']
            reply = make_reply(message)

            #Send the message
            bot.send_message(reply, from_)