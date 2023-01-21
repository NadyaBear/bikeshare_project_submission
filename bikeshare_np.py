from operator import index
import time
from tkinter.messagebox import YES
import pandas as pd
import numpy as np

# Numpy 1.20.1
# Pandas 1.2.4 - a little buggy with mode()


#Defining User Input Options
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). 
    city_name = ' '
    while city_name.lower() not in CITY_DATA:
        city_name = input("""\nWhat city's data would you like to analyze? \n(Pick one of the following: chicago, new york city, or washington)\n""")
        if city_name.lower() in CITY_DATA:
            city = city_name.lower()
        else:
            print("""\n Oops! This city's data is not available. Please check your spelling and choose from the provided list.\n""")
            
    # Get user input for month (all, january, february, ... , june)
    month_name = ' '
    while month_name.lower() not in MONTH_DATA:
        month_name = input("""\nWhat is the name of the month you would like to analyze? \n(Pick one of the following: january, february, march, april, may, june, or all)\n""")
        if month_name.lower() in MONTH_DATA:
            month = month_name.lower()
        else:
            print("""\nOops! This month's data is not available. Please check your spelling and choose from the provided list.\n""")


    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day_name = ' '
    while day_name.lower() not in DAY_DATA:
        day_name = input("""\n What is the day of the week you would like to analyze? \n(Pick one of the following: monday, tuesday, wednesday, thursday, friday, saturday, sunday, or all)\n""")
        if day_name.lower() in DAY_DATA:
            day = day_name.lower()
        else: 
            print("""\nOops! This day's data is not available. Please check your spelling and choose from the provided list. \n""")
            

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Load dataframe using pandas module
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    df = df

    #Filter df by user input for 'month'
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        #edit to correspond value of input to appropriate index
        index = months.index(month)+1 
        month = index
        df = df[df['month'] == month]

    #Filter df by user input for 'day'
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        #edit to correspond value of input to appropriate index
        index = days.index(day) 
        day = index
        df = df[df['day'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    

    start_time = time.time()

    # Display the most common month   
    common_month = df['month'].mode()[0]
    months = {1:'january',2:'february',3:'march',4:'april',5:'may',6:'june'}
    print("The most common month is:", str(months[common_month]).title())

    # Display the most common day of week
    common_day = df['day'].mode()[0]
    days = {0:'monday',1:'tuesday',2:'wednesday',3:'thursday',4:'friday',5:'saturday',6:'sunday'}
    print("The most common day is:", str(days[common_day]).title())

    # Display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("The most common hour is: {}:00 military time.".format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common station to start at is:", common_start_station)

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common station to end at is:", common_end_station)

    # Display most frequent combination of start station and end station trip
    common_start_and_end_station = (df['Start Station'] + '+' + df['End Station']).mode()[0]
    print("The most common station to start and end at is:", common_start_and_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    # Adjust time scale to reflect friendly time_scale annotation
    total_travel_time = df['Trip Duration'].sum()
    if total_travel_time > 86400:
        total_travel_time = round(total_travel_time/86400)
        time_scale = 'days'
    elif total_travel_time >3600:
        average_travel_time = round(average_travel_time/3600)
        time_scale = 'hours'
    elif total_travel_time>60: 
        average_travel_time = round(average_travel_time/60)
        time_scale = 'minutes'
    else:
        time_scale = 'seconds'
    print("Total Travel Time is: {} {}".format(total_travel_time, time_scale))

    # Display mean travel time
    # Adjust time scale to reflect friendly time_block annotation
    average_travel_time = df['Trip Duration'].mean()
    if average_travel_time >360:
        average_travel_time = round(average_travel_time/360)
        time_block = 'hours'
    elif average_travel_time>60: 
        average_travel_time = round(average_travel_time/60)
        time_block = 'minutes'
    else:
        time_block = 'seconds'
    print("Average Travel Time is: {} {}".format(average_travel_time, time_block ))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print('User Types:\n',count_user_type,'\n')

    #Create a condition to display gender data only when it's available
    if city=='washington':
        print('No Gender Data for {}'.format(city).title())
    else:
        # Display counts of gender
        count_gender = df['Gender'].value_counts()
        print('Gender Demographic:\n',count_gender,'\n')

        # Display earliest, most recent, and most common year of birth
        dob_earliest = int(df['Birth Year'].min())
        dob_recent = int(df['Birth Year'].max())
        dob_common = int(df['Birth Year'].mode()[0])
        print('The Earliest DOB Year is:', dob_earliest)
        print('The Latest DOB Year is:', dob_recent)
        print('The Most Common DOB Year is:', dob_common)
        
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Display raw data 5 rows at a time. """

    start_row = 0
    raw = input("Would like to see the raw data?").lower() 
    pd.set_option('display.max_columns',200)

    additional_data = True
    while additional_data:          
        print(df.iloc[start_row:(start_row+5)]) # TO DO: appropriately subset/slice your dataframe to display next five rows
        start_row += 5
        raw = input("Would like to see 5 more rows?").lower() 
        if raw == "no":    
            additional_data = False

#Synthesize the above functions to run within main
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        
if __name__ == "__main__":
	main()
