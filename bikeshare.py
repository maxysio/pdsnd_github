import time
import pandas as pd
import numpy as np
import calendar
from scipy import stats
import os

#global lists
city_list = {'chicago': 1, 'washington': 2, 'new york': 3, '1': 1, '2': 2, '3': 3}
city_file = {1: 'chicago.csv', 2: 'washington.csv', 3: 'new_york_city.csv'}
month_list = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11,
                'december': 12, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11,
                'dec': 12, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12}
day_month_list = {'day': 1, 'month': 2, 'both': 3, 'none': 4, '1': 1, '2': 2, '3': 3, '4': 4}
day_list = {'sunday': 6, 'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, '1': 6, '2': 0, '3': 1, '4': 2, 
                '5': 3, '6': 4, '7': 5, 'sun': 6, 'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5}
city_name = {1: 'Chicago', 2: 'Washington DC', 3: 'New York City'}


def get_datafilters():
    city, month, day = -1, -1, -1
    
    #Get the city
    invalid_input = True
    while(invalid_input):
        city_name = input('\nWhich city would you like to see the data analysis for - Chicago(1), Washington(2) or New York(3)\n')
        city = city_list.get(city_name.lower(), -1)
        if(city>0):
            invalid_input = False
        else:
            print('That doesn\'t look like a valid selection. Lets try again')

    #Check how they want to filter
    invalid_input = True
    while(invalid_input):
        date_or_month = input('\nWould you like to filter by month(1), day(2), both(3) or none at all(4)\n')
        date_or_month = day_month_list.get(date_or_month.lower(), -1)
        if(date_or_month>0):
            invalid_input = False
        else:
            print('That doesn\'t look like a valid selection. Lets try again')

    #Get the month
    if(date_or_month == 1 or date_or_month == 3):
        invalid_input = True
        while(invalid_input):
            month = input('\nChoose a month you want to filter data by: January, February, March...etc. You can use numbers or 3 letter notations\n')
            month = month_list.get(month.lower(), -1)
            if(month>0):
                invalid_input = False
            else:
                print('That doesn\'t look like a valid selection. Lets try again')
    
    #Get the day
    if(date_or_month == 2 or date_or_month == 3):
        invalid_input = True
        while(invalid_input):
            day = input('\nChoose a day you want to filter data by: Sunday(1), Monday(2)...Saturday(7)\n')
            day = day_list.get(day.lower(), -1)
            if(day>-1):
                invalid_input = False
            else:
                print('That doesn\'t look like a valid selection. Lets try again')

    return city, month, day

def load_data(city, month, day):
    
    #get the current directory of the python script
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    #filter by city first
    df = pd.read_csv(os.path.join(__location__, city_file.get(city)))

    # add columns for Month and Day of Week
    df['Month'] = pd.DatetimeIndex(pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')).month
    df['DayOfWeek'] = pd.DatetimeIndex(pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')).dayofweek
    
    #filter by month if applicable
    if(month>-1):
        df = df[df['Month'] == month]

    #filter by day if applicable
    if(day>-1):
        df = df[df['DayOfWeek'] == day]

    return df

def raw_data(df):
    show_raw_data = input('Would you like to see the raw data? (Yes(Y)/No(N)): ').lower()
    if(show_raw_data=='y' or show_raw_data=='yes'):
        number_of_lines = input('How many lines would you like to see? ')
        try:
            number_of_lines = int(number_of_lines)
        except ValueError:
            print('That does not look like a number, so we will show the first 5 lines')
            number_of_lines = 5
        
        print(df.head(number_of_lines))

def time_stats(df):
    print('-'*40)
    print('Time stats coming up')
    print('-'*20)
    # display the most common month
    print('The most popular month: ' + calendar.month_name[df['Month'].mode()[0]])

    # display the most common day of week
    print('The most popular day of the week: ' + calendar.day_name[df['DayOfWeek'].mode()[0]])

    # display the most common start hour
    df['Hour'] = pd.DatetimeIndex(pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')).hour
    most_common_hour = pd.to_datetime(str(df['Hour'].mode()[0]), format='%H')
    print('The most popular hour: ' + most_common_hour.strftime('%I %p'))

    print('-'*40)

def station_stats(df):
    print('-'*40)
    print('Station stats coming up')
    print('-'*20)
    
    #print most popular starting station
    print('The most popular starting station is: ' + df['Start Station'].mode()[0])

    #print most popular ending station
    print('The most popular ending station is: ' + df['End Station'].mode()[0])

    #print most popular trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most popular trip: ' + df['Trip'].mode()[0])

    print('-'*40)

def trip_duration_stats(df):
    print('-'*40)
    print('Trip Duration stats coming up')
    print('-'*20)
    
    #print Total Travel time
    h, m , s = 0, 0, 0
    m, s = divmod(df['Trip Duration'].sum(), 60)
    h, m = divmod(m, 60)
    p = 'Total travel time was: '
    if(h>0):
        p += str(h) + ' hours, '
    elif(m>0):
        p += str(m) + ' minutes, '
    print(p + str(s) + ' seconds')

    #print average Travel time
    h, m , s = 0, 0, 0
    m, s = divmod(df['Trip Duration'].mean(), 60)
    h, m = divmod(m, 60)
    p = 'Average travel time was: '
    if(h>0):
        p += str(h) + 'hours, '
    elif(m>0):
        p += str(m) + ' minutes, '
    print(p + str(s) + ' seconds')

    print('-'*40)

def user_stats(df, city):
    print('-'*40)
    print('User stats coming up')
    print('-'*20)
    
    #Counts of each user type
    df1 = df.groupby('User Type')['User Type'].count()
    if(df1.size>0):
        print('User Type ---> Number of Users')
        for x in range(df1.size):
            print(df1.index[x] + ' ---> ' + str(df1[x]))
        print('-'*20)

    #Following are applicable for Chicago and NYC
    if(city==1 or city==3):

        if(exit_app()):
            return
        else:
            #Group By Gender
            df2 = df.groupby('Gender')
            
            #Counts of each gender (only if NYC and Chicago)
            df3 = df2['Gender'].count()
            if(df3.size> 0):
                print('-'*20)
                print('Gender ---> Number of')
                print('-'*20)
                for x in range(df3.size):
                    print(df3.index[x] + ' ---> ' + str(df3[x]))
                print('-'*20)


        if(exit_app()):
            return
        else:
            #Earliest year of birth
            df3 = df2['Birth Year'].min()
            if(df3.size> 0):
                print('-'*20)
                print('Gender ---> Earliest Birth Year')
                print('-'*20)
                for x in range(df3.size):
                    print(df3.index[x] + ' ---> ' + str(df3[x]))
                print('-'*20)


        if(exit_app()):
            return
        else:
            #Most recent year of birth
            df3 = df2['Birth Year'].max()
            if(df3.size> 0):
                print('-'*20)
                print('Gender ---> Most Recent Birth Year')
                print('-'*20)
                for x in range(df3.size):
                    print(df3.index[x] + ' ---> ' + str(df3[x]))
                print('-'*20)


        if(exit_app()):
            return
        else:
            #Most common year of birth
            df3 = df2['Birth Year'].agg(lambda x: stats.mode(x))
            if(df3.size> 0):
                print('-'*20)
                print('Gender ---> Most Common Birth Year')
                print('-'*20)
                for x in range(df3.size):
                    print(df3.index[x] + ' ---> ' + str(df3[x][0]))
                print('-'*20)
    
def exit_app():
    done = input('Do you want to see stats or do you want to exit the application? Enter Yes or y to keep going: ').lower()
    if(done =='yes' or done =='y'):
        return False
    else:
        return True

def main():
    while True:
        #Get user input on how the data should be processed
        city, month, day = get_datafilters()

        print('Crunching data for the following: \nCity: {}'.format(city_name.get(city)))
        if(month>-1):
            print('Month: {}'.format(calendar.month_name[month]))
        if(day>-1):
            print('Day: {}'.format(calendar.day_name[day]))

        df = load_data(city, month, day)

        # Raw Data
        raw_data(df)

        if(exit_app()):
            break
        else:
            # Compute Popular times of travel 
            time_stats(df)

        if(exit_app()):
            break
        else:
            # Popular stations and trip
            station_stats(df)

        if(exit_app()):
            break
        else:
            # Trip duration
            trip_duration_stats(df)

        if(exit_app()):
            break
        else:
            # User info
            user_stats(df, city)

        restart = input('\nWe have computed all the statistics. Would you like to start again or quit the application? Enter yes(y) or no(n) or pretty much anything other than y).\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break

    print('\nThank you for trying out the application. Hope to see you again\n')

if __name__ == "__main__":
	main()
