import pandas as pd 
import numpy as np 
from datetime import datetime, timedelta

#Helper function to format time deltas as strings
def format_time_delta(duration):

    seconds = duration.seconds
    hours = int(seconds / 3600)
    remaining = seconds % 3600
    minutes = int(remaining / 60)
    remaining = remaining % 60
    seconds = int(remaining)

    if hours == 0:
        out = '{}min {}s'.format(minutes, seconds)
    else:
        out = '{}h {}min {}s'.format(hours, minutes, seconds)
    
    return out

def round_time(time):
    return time - timedelta(microseconds = time.microsecond)

class StudyTracker():

    #Constructor method
    def __init__(self):
        try:
            self.df = pd.read_csv('studytime.csv', parse_dates = ['Start', 'End'])
        except:
            self.df = pd.DataFrame(columns = ['Start', 'End', 'Duration', 'Subject', 'Task'])
        
        self.current_task_name = None
        self.start_time = None
        self.end_time = None

    #Saves the dataframe into CSV file
    def save_csv(self):
        self.df.to_csv('studytime.csv', index = False)

    #Starts a task

    def start_task(self, subject_name, task_name):
        self.current_task_name = task_name
        self.current_subject_name = subject_name
        self.start_time = datetime.now()

        return 'Started {} at {}'.format(task_name, round_time(self.start_time))
    
    #Ends a task - asks you for the productivity rating

    def end_task(self):
        if self.current_task_name is not None:
            end_time = datetime.now()
            duration = end_time - self.start_time

            self.df = self.df.append({'Start': self.start_time, 'End': end_time, 'Duration': duration, 'Subject': self.current_subject_name, 'Task': self.current_task_name}, ignore_index = True)

            print('duration is')
            print(duration)

            #Get subset of today's study sessions
            today_sessions = self.df['Start'].apply(lambda x: x.date() == end_time.date())
            df_filtered = self.df.loc[today_sessions, :]

            today_duration = (df_filtered['End'] - df_filtered['Start']).sum()

            out = '''
            Ended {} at {}
            Time Spent: {}
            Study Time Today: {}
            '''.format(self.current_task_name, round_time(end_time), format_time_delta(duration), format_time_delta(today_duration))

            print(self.df)

            self.current_subject_name = None
            self.current_task_name = None
            self.start_time = None

            self.save_csv()

            return out

    def get_summary(self):
        
        date_now = datetime.now()

        #Get subset of today's study sessions
        today_sessions = self.df['Start'].apply(lambda x: x.date() == date_now.date())
        df_filtered = self.df.loc[today_sessions, :]

        today_duration = (df_filtered['End'] - df_filtered['Start']).sum()

        #5 days average
        date_min = date_now - timedelta(days = 5)

        is_filtered_dates = (self.df['Start'] > date_min) & (self.df['Start'] < date_now)
        df_filtered_5days = self.df.loc[is_filtered_dates, :]

        five_day_average_duration = (df_filtered_5days['End'] - df_filtered_5days['Start']).sum() / 5

        #7 days ago

        #Top subjects studied
        self.df['Duration'] = self.df['End'] - self.df['Start']
        subjects = self.df.groupby('Subject')['Duration'].sum()
        subjects_summary = ''
        for subject, duration in subjects.iteritems():
            subjects_summary += '{}: {} \n'.format(subject, format_time_delta(duration))

        
        out = '''
        Study Summary for {}
Study Time: {}
5-day Average: {}
Subjects:
{}
        '''.format(date_now.strftime('%m/%d'), format_time_delta(today_duration), format_time_delta(five_day_average_duration), subjects_summary)

        return out
