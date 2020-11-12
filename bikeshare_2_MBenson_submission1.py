import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs


    city = input('Would you like to see data for Chicago, New York city, or Washington?   ')
    while city.title() not in ['Chicago', 'New York City', 'Washington']:
    	print("Your input '{}' doesnt seem to match one of the options. Please try again".format(city))
    	city = input('Would you like to see data for Chicago, New York city, or Washington?   ') 

    option = input("Would you like to filter the data by 'month', 'day', or 'both' (month and day) or 'none' (not at all)?   ")	
    while option.title() not in ['Month', 'Day', 'Both', 'None']:
        print("Your input '{}' doesnt seem to match one of the options. Please try again".format(city))
        option = input("Would you like to filter the data by 'month', 'day', or 'both' (month and day) or 'none' (not at all)?   ")

    if option.title() in ['Both', 'Month']: 
	    # get user input for month (all, january, february, ... , june)
	    month = input('Which month? January, February, March, April, May, or June?   ')
	    while month.title() not in ['January', 'February', 'March', 'April', 'May', 'June']:
	    	print("Your input '{}' doesnt seem to match one of the options. Please try again".format(month))
	    	month = input('Which month? January, February, March, April, May, or June?   ')
    else:
	    month = 'all'

    if option.title() in ['Both', 'Day']:
	    # get user input for day of week (all, monday, tuesday, ... sunday)
	    day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?   ')
	    while day.title() not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
	        print("Your input '{}' doesnt seem to match one of the options. Please try again".format(day))
	        day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?   ')
    else:
	    day = 'all'

    #MB TEST
    print('\nSelected filters for city, month, day are: {}, {}, {}'.format(city, month, day))

    print('-'*40)
    return city.lower(), month.lower(), day.lower()
   

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week(#)'] = df['Start Time'].dt.weekday
    df['start_hr'] = df['Start Time'].dt.hour
    #df['day_of_week(a)'] = df['Start Time'].dt.day_name

    df['station_combo'] = df['Start Station']+", going to "+df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = {'monday': int(0), 'tuesday': int(1), 'wednesday': int(2), 'thursday': int(3), 'friday': int(4), 'saturday': int(5), 'sunday': int(6)}
        day = days[day]
        df = df[df['day_of_week(#)']==day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month ('mcm')
    mcm = MONTHS[df['month'].mode()[0]-1]
    print("The most common month is:  {}".format(mcm))

    # display the most common day of week ('mcdow')
    mcdow = WEEKDAYS[df['day_of_week(#)'].mode()[0]]
    print("The most common day of the week is: {}".format(mcdow))

    # display the most common start hour ('mcsh')
    mcsh = df['start_hr'].mode()[0]
    print("The most common start hour is: {}00 hours".format(mcsh))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station ('mcss')
    mcss = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}".format(mcss))

    # display most commonly used end station ('mces')
    mces = df['End Station'].mode()[0]
    print("The most commonly used end station is: {}".format(mces))

    # display most frequent combination ('mfcombo') of start station and end station trip
    mfcombo = df['station_combo'].mode()[0]
    print("The most frequent combination of start station and end station trip is: {}".format(mfcombo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time ('ttt')
    ttt = df['Trip Duration'].sum()
    print("The total travel time : {}".format(ttt))

    # display mean travel time ('mtt')
    mtt = df['Trip Duration'].mean()
    print("The mean travel time is: {}".format(mtt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subscribers = df['User Type'].value_counts()['Subscriber']
    customers = df['User Type'].value_counts()['Customer']
    print("The split of user types (Subscribers: Customers) is:  {}: {}".format(subscribers, customers))

    if city.title() == 'Washington':
        print("No gender or age statistics available for Washington")

    else:
        # Display counts of gender
        male_users = df['Gender'].value_counts()['Male']
        female_users = df['Gender'].value_counts()['Female']
        print("The gender split is:  Male users = {}, Female users = {}".format(male_users,female_users))

        # Display earliest ('yob_e'), most recent ('yob_mr'), and most common ('yob_mc') year of birth
        yob_e = int(df['Birth Year'].min())
        yob_mr = int(df['Birth Year'].max())
        yob_mc = int(df['Birth Year'].mode()[0])
        print("The earliest, most recent and most common birth year is:  {}, {}, {}".format(yob_e,yob_mr,yob_mc))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    want_to_see = input("Would you like to see 5 lines of raw data? ['Yes'/'No'] ")
    while want_to_see.title() not in ['Yes', 'No']:
        print("Your input '{}' doesnt seem to match one of the options. Please try again".format(want_to_see))
        want_to_see = input("Would you like to see 5 lines of raw data? ['Yes'/'No'] ")
    i=0
    while want_to_see.title() == 'Yes':
        print(df[i:i+5])
        i+=5
        want_to_see = input("Would you like to see 5 more lines of raw data? ['Yes'/'No'] ")    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
