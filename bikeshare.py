import time
# import only system and name from os - used by clear_screen function.
from os import system, name as os_name 
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv', 
            }

month_list = [ 'all','january','february',
              'march','april', 'may','june', 
             ]

def clear_screen():
    """
    Clears the terminal screen using the relevant OS system command
    """
    # Referenced https://www.geeksforgeeks.org/clear-screen-python/ 
    # for clear screen function code below
    # for windows:
    if os_name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix'):
    else:
        _ = system('clear')
        
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) city_csv - name of the city CSV FILE to analyze
        (str) month - name of the month to filter by, 
            or "all" to apply no month filter
        (str) day - name of the day of week to filter by, 
            or "all" to apply no day filter
    """
    # I changed the output of the function to return the CSV file as
    # we are already calling on the dictionary to check the names.

    reloop = True 
    # Get cities from CITY_DATA so that any new data files are only 
    # added/updated in one place.
    city_list = [key for key in CITY_DATA]  

    # List of options when selecting the day filter options
    day_list =   [ 'all', 'monday',
                  'tuesday', 'wednesday',
                  'thursday', 'friday', 
                  'saturday', 'sunday',
                 ]

    clear_screen()
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*40)
    # Get user input for city (chicago, new york city, washington).
    # The idea of having to type a city name correctly drives me crazy:
    # therefore I have added the option to use numbers as well.
    # Note that I left the ability to type the full words as I assume
    # this is required as part of the assessment. It was interesting to
    # make it work for multiple types of input in any case.

    # Create list of cities to provide to user.
    output_text = ''
    for i, value in enumerate(city_list):
        output_text = output_text + "\n {}. {}".format(i + 1, value.title())   
    print('Data exists for the following US Cities:{}'.format(output_text))

    while reloop:
        # Get the input as a string into city_name.
        city_name = input('Please select the city by entering the '
                          + 'corresponding number or name: ')
        reloop = False
        try:
            # Check to see if it is an integer.
            city_id = int(city_name)
        except:
            reloop = True
        else:
            if city_id > 0 and city_id < 4:
                # Get name to use it below.
                city_name = city_list[city_id - 1] 
                city_csv = CITY_DATA[city_name.lower()]
                # End While Loop as value found.
                break 
            print('That is an invalid option, please enter an integer '
                  + 'between 1 and 3 or the name of the city.')
            reloop = True
            # End while loop iteration as value is not a string.
            continue 
        try:
            # If the input is not an integer, check to see if it is 
            # an option in the CITY_DATA dictionary.
            city_csv = CITY_DATA[city_name.lower()]
            # End while loop as value found.
            break 
        except:
            print('That is an invalid option, please enter an integer between '
                  + '1 and 3 or the name of the city.')
            # Reset the while value to continue looping.
            reloop = True

    time.sleep(.5)
    clear_screen()
    print("City selected: {}".format(city_name.title()))
    
    # Get filter options from user:
    filter_month, filter_day = filter_options(city_name)

    if filter_month:
        # Get user input for month (all, january, february, ... , june).
        print('-'*40 + '\nSelect which month to filter the data by '
              + '(only Jan - Jun available).\n'
              + 'For more information on options enter \'?\':')

        # Again I've added the option for numbers, but I found listing 
        # the options by default a bit much, so added the ability for 
        # the user to ask for them.
        reloop = True
        while reloop:
            # Get input as a string into month
            month = input('Please enter the month name or number: ' )
            reloop = False
            # Print list of options if '?' was entered
            if month == '?':
                reloop = True
                print('Available Options\n' + '-'*18)
                for index, value in enumerate(month_list):
                        print(' {}. {}'.format(index, value.title()))

                # End while loop iteration asking for options only.
                continue 
            try:
                # Check to see if it is an integer
                month_list_id = int(month)
            except:
                reloop = True
            else:
                if month_list_id == 0:
                    # Check if user picked all deliberately.
                    sub_reloop = True
                    while sub_reloop:
                        check_all = input('You have selected \'0. All\' to '
                                      + 'filter on all months.\nIs that correct'
                                      + '?\n(Y)es or (N)o: ') 
                        # got sick of mis-typing yes so shortened to 'y'.
                        try:
                            # Check that restart is not an empty string.
                            check_response = check_all[0].lower()
                        except:
                            print('Invalid entry, please try again.')
                            # Get another input if empty string.
                            continue
                        else:
                            # Exit this loop if a string is received.
                            sub_reloop = False

                    if check_all[0].lower() == 'y':
                        month = month_list[month_list_id]
                        print("Month option selected: {}".format(
                            month.title()))
                        # End while loop as value found.
                        break 
                    else:
                        reloop = True
                        # End while loop iteration to get a new input
                        # value for the month.
                        continue 
                elif month_list_id > 0 and month_list_id < 7:
                    month = month_list[month_list_id]
                    print("Month option selected: {}".format(month.title()))
                    # End while loop as value found.

                    break 
                else:
                    reloop = True # Reloop if value not found.
                    print('That is not a valid option, please enter an '
                          + 'integer between 1 and 6 or the full name '
                          + 'of the month.')
                    print('Enter \'?\' for a list of options.')
                    # End while loop iteration as integer not in the
                    # correct range.
                    continue 
            try:
                # If the input is not an integer, check to see if it is 
                # an option in the month list.

                check_month = month_list.index(month.lower())
            except:
                print('That is not a valid option, please enter an integer '
                      + 'between 1 and 6 or the full name of the month.')
                print('Enter \'?\' for a list of options.')

                # No valid option found, reloop
                reloop = True
            else:
                # Confirm selection of All.
                if month.lower() == 'all':
                    # Check if user picked all deliberately.
                    sub_reloop = True
                    while sub_reloop:
                        check_all = input('You have selected \'0. All\' to '
                                      + 'filter on all months.\nIs that '
                                      + 'correct?\n(Y)es or (N)o: ')
                        # got sick of mis-typing yes so shortened to 'y'.
                        try:
                            # Check that restart is not an empty string.
                            check_response = check_all[0].lower()
                        except:
                            print('Invalid entry, please try again.')
                            # Get another input if empty string.
                            continue
                        else:
                            # Exit this loop if a string is received.
                            sub_reloop = False
                            
                    if check_all[0].lower() != 'y':
                        reloop = True
                        continue
                    
                # Option found.
                reloop = False
                print("Month option selected: {}".format(
                    month.title()))               
    else:
        # Added additional call here to set month = 'all' just in case.
        month = 'all'

    if filter_day:
        # Get user input for day of week if filter by day was 
        # selected (monday, tuesday, ... sunday).
        # Pretty much a copy of month filter input above.
        print('-'*40 + '\nSelect the day of the week to filter the data by.\n'
              + 'For available options enter \'?\':')

        reloop = True
        while reloop:
            # Get input as a string into day.
            day = input('Please enter the day name or number (Monday = 1): ' )
            reloop = False
            # Print list of options if '?' was entered.
            if day == '?':
                reloop = True
                print('Available Options\n' + '-'*18)
                for index, value in enumerate(day_list):
                        print(' {}. {}'.format(index, value.title()))
                # End while loop iteration asking for options only.
                continue 

            try:
                # Check to see if it is an integer.
                day_list_id = int(day)
            except:
                reloop = True
            else:
                if day_list_id == 0:
                    
                    # Check if user picked all deliberately.
                    sub_reloop = True
                    while sub_reloop:
                        check_all = input('You have selected \'0. All\' to '
                                      + 'filter on all days.\nIs that correct'
                                      + '?\n(Y)es or (N)o: ')
                        # got sick of mis-typing yes so shortened to 'y'.
                        try:
                            # Check that restart is not an empty string.
                            check_response = check_all[0].lower()
                        except:
                            print('Invalid entry, please try again.')
                            # Get another input if empty string.
                            continue
                        else:
                            # Exit this loop if a string is received.
                            sub_reloop = False

                    if check_all[0].lower() == 'y':
                        day = day_list[day_list_id]
                        print("Day option selected: {}".format(day.title()))
                        # End while loop as value found.
                        break 
                    else:

                        reloop = True
                        # End while loop iteration to get a new input
                        # value for the day.
                        continue 
                elif day_list_id > 0 and day_list_id < 8:
                    day = day_list[day_list_id]
                    print("Day option selected: {}".format(day.title()))
                    # End while loop as value found.
                    break 
                else:
                    # Reloop if value not found.
                    reloop = True 
                    print('That is not a valid option, please enter an integer'
                          + ' between 1 and 7 or the full name of the day.')
                    print('Enter \'?\' for a list of options.')
                    # End while loop iteration as integer not in the 
                    # correct range.
                    continue 
            try:
                # If the input is not an integer, check to see if it is 
                # an option in the day list.

                check_day = day_list.index(day.lower())
                reloop = False
            except:
                print('That is not a valid option, please enter an integer'
                      + ' between 1 and 7 or the full name of the day.')
                print('Enter \'?\' for a list of options.')
                # No valid option found, reloop.
                reloop = True
            else:
                
                # Confirm selection of All.
                if check_day == 0:
                    # Check if user picked all deliberately.
                    sub_reloop = True
                    while sub_reloop:
                        check_all = input('You have selected \'0. All\' to '
                                      + 'filter on all days.\nIs that correct'
                                      + '?\n(Y)es or (N)o: ')
                        # got sick of mis-typing yes so shortened to 'y'.
                        try:
                            # Check that restart is not an empty string.
                            check_response = check_all[0].lower()
                        except:
                            print('Invalid entry, please try again.')
                            # Get another input if empty string.
                            continue
                        else:
                            # Exit this loop if a string is received.
                            sub_reloop = False

                    if check_all[0].lower() != 'y':
                        reloop = True
                        continue
                    else:
                        # Option found.
                        print("Day option selected: {}".format(day.title()))
    else:
        # Set day to all here just in case
        day = 'all'

    # Pause for 1 second before clear screen for summary info.
    print('Screen will clear for filter Summary Information...')
    time.sleep(1) 
    clear_screen()
    
    return city_name, city_csv, month, day

def filter_options(city_name):
    """
    Get user input to filter on Month or Day of the Week
    
    Arguments:
        (str) - city_name - the name of the city selected for the filter
    
    Returns:
        bool - filter_month - whether to filter on month or not
        bool - filter_day - whether to filter on day or not
    """
    # Create the filter options list:
    filter_options = ['None', 'Month',
                      'Day', 'Both Month & Day',
                     ]
    # Determine if the function will ask for month or day:
    filter_month, filter_day = False, False 
    
    filter_options_text = ''
    # Print options header
    print('-'*40 + '\nWhich filter would you like to apply to the '
          + '{} data?'.format(city_name.title()))
    # Iterate through filter_options list and format ready to print
    for index, options in enumerate(filter_options):
        filter_options_text = filter_options_text + "\n {}. {}".format(
            index + 1, options)
    # Print filter_options_text for user to pick from
    print('Available Options:\n' + '-'*18 + '{}'.format(filter_options_text))
    reloop = True

    while reloop:
        #Get input on filtering options.
        reloop = False
        filter_op = input('Please enter the filter option name or number: ')
        try:
            # Check to see if an interger.
            filter_id = int(filter_op)
        except:
            # not an integer - set reloop in case not a string.
            reloop = True
        else:
            if filter_id > 0 and filter_id < 5:
                # Get name to use it below.
                filter_name = filter_options[filter_id - 1] 
                # End While Loop as value found.
                break 
            print('That is an invalid option, please enter an integer between '
                  + '1 and 3 or the name of the city.')
            reloop = True
            # End while loop iteration as value is not a string.
            continue 
        try:
            # If the input is not an integer, check to see if it is 
            # an option in the filter_options list.
            filter_id = filter_options.index(filter_op.title())
        except:
            print('That is an invalid option, please enter an integer between '
                  + '1 and 4 or the name of the option.')
            # Reset the while value to continue looping
            reloop = True
        else:
            filter_name = filter_options[filter_id]
            # End while loop as value found.
            break  
    
    time.sleep(.5)
    clear_screen()
    print('Filter Option selected: {}'.format(filter_name))
    
    # Only ask for further parameters based on filter option selected.
    # Match options to filter_options.

    if filter_name.lower() == 'none':
        # No filtering on Month or Day.
        month = 'all'
        day = 'all'
    elif filter_name.lower() == 'month':
        # No filtering on Day - filtering on Month.
        filter_month = True
        day = 'all'
    elif filter_name.lower() == 'day':
        # No filtering on Month - filtering on Day.
        month = 'all'
        filter_day = True
    elif filter_name.lower() == 'both month & day':
        # Filter on both month and day
        filter_month = True
        filter_day = True
    else:
        # Force filter selection on both - should never occur, 
        # but I prefer an else statement in this case.
        filter_month = True
        filter_day = True

    return filter_month, filter_day

def display_filter(city_name, month, day):
    """
    Displays the filter options that were selected for the statisitical 
    information.
    
    Arguments:
        (str) city_name - name of the city being analyzed.
        (str) month - name of the month filter, or "all" for no month filter.
        (str) day - name of the day of week filter, or "all" for no day filter.
    """

    # Output filter options selected:
    print('-'*43)
    print('FILTER SELECTIONS:')
    print('-'*43)
    print('City selected:\t\t{}'.format(city_name.title()))
    print("Month option selected:\t{}".format(month.title()))
    print("Day option selected:\t{}".format(day.title()))
    print('-'*43 + '\n')
    

def continue_to_stats():
    """
    Gets input to determine if the user would like to continue with the 
    program, restart, or end the program.
    
    Returns:
        (str) continue_bikeshare - value selected to continue after getting 
            inputs - yes, no, or restart
    """

    # Check if user wants to continue:
    reloop = True
    while reloop:
        print('Do you want to continue to view the general information for the '
              + 'selected filter?\nAvailable options:')
        print('-'*18 + '\n - (y)es\n - (n)o\n - (re)start')
        check_all = input('Enter option: ')
        try:
            check_response = check_all[0].lower()
        except:
            print('Invalid entry, please try again')
            continue
        else:
            reloop = False
            if check_response == 'y':
                continue_bikeshare = 'yes'
            elif check_all[0:2].lower() == 're':
                continue_bikeshare = 'restart'
            else:
                continue_bikeshare = 'no'
                
    return continue_bikeshare       


def load_data(city_csv, month, day):
    """
    Loads data for the specified city data and filters by month and day if 
    applicable.

    Arguments:
        (str) city_csv - name of the city CSV FILE to analyze
        (str) month - name of the month to filter by, or "all" to apply no 
            month filter
        (str) day - name of the day of week to filter by, or "all" to apply 
            no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv('./{}'.format(city_csv), index_col = 0)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Calculate month from Start Time and create new column in df.
    df['Month'] = df['Start Time'].dt.month
    
    # Calculate weekday from Start Time and create new column in df.
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # Filter df by the month if it is not all.
    if month !='all':        
        # Apply filter to month column and update df dataset using 
        # global list month_list.
        # Note that month_list has been configured that the index = 
        # month number (no offset required).
        df = df[df.Month == month_list.index(month)]

    # Filter df by the day if it is not all
    if day !='all':
        # Apply filter to day column and update df dataset using day.
        df = df[df.day_of_week == day.title()]

    return df
    

def general_info(df, city_name):
    """
    Displays general information for the filtered data including the ability 
    to scroll through raw data.
    
    Arguments:
        df - pandas dataframe - contains the filtered ride share data for the
             selected city.
        (str) city_name - name of the city being analyzed.
    """

    print('-'*43)
    print('GENERAL INFORMATION:')
    print('-'*43)
    
    print('\nCalculating General Information...')
    start_time = time.time()
    
    total_records = df['End Time'].count()
    print('Total Trips in filtered list:    {}'.format(
        df['End Time'].count()))

    print("\nCalculation of General Information took %s seconds." % (
        time.time() 
        - start_time))

    display = True
    while display == True:
        see_data = input('Would you like to see the first five rows '
                         + 'of underlying raw data in '
                         + 'the filtered list? (y)es or (n)o: ')
        try:
            check_response = see_data[0].lower()
        except:
            print('Invalid entry, please try again.')
            continue
        else:
            display = False
    
    if see_data[0].lower() == 'y':
        # Start by displaying the first 5 rows of data
        display = True
        row_num = 5
        
        print("Displaying row {} to row {} of {} rows of data".format(
            row_num - 4, row_num, total_records))
        print(df[0:5])
        message = ''
        while display == True:
            message = '\nDo you want display 5 more rows (y), 20 (m)ore '
            message = message + 'rows, (a)ll remaining {}'.format(
                total_records - row_num)
            message_add = 'rows, or (s)top displaying the data?'
            message_add = message_add + '\nSelecting to display all '
            message_add = message_add + 'records will be limited in large data'
            message_add = message_add + ' sets.\nPlease enter an option (y)es/'
            message_add = message_add +  '(m)ore/(a)ll/(s)top: '

            continue_response = input('{} {}'.format(message, message_add))
            start_row_num = row_num
            row_num = row_num + 5
            # Check response and run as requested:
            try:
                check_response = continue_response[0].lower()
            except:
                print('Invalid entry, please try again.')
                continue
            else:
                if check_response == 'y':
                    if row_num >= total_records:
                        row_num = total_records
                        display = False
                    print("Displaying row {} to row {} of {} ".format(
                        start_row_num + 1, 
                        row_num, 
                        total_records) + 
                        'rows of data.')

                    print(df[start_row_num:row_num])
                elif check_response == 'm':
                    row_num = row_num + 15
                    if row_num >= total_records:
                        row_num = total_records
                        display = False
                    print("Displaying row {} to row {} of {} ".format(
                        start_row_num + 1,
                        row_num,
                        total_records) +
                        'rows of data.')
                    print(df[start_row_num:row_num])
                elif check_response == 'a':
                    print(df[start_row_num:])
                    print('All remaining data displayed as per program ' 
                          + 'display rules.')
                    display = False
                else:
                    display = False
        continue_response = input('Hit Enter to see more statisitical ' 
                                  + 'information on the {}'.format(
                                      city_name.title())
                                  + ' Bikeshare data.')

    
def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.
    
    Arguments:
        df - pandas dataframe - contains the filtered ride share data for the 
             selected city.
        (str) month - name of the month filter, or "all" for no month filter.
        (str) day - name of the day of week filter, or "all" for no day filter.
    """

    print('-'*43)
    print('TIME STATISTICS:')
    print('-'*43)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #print(df.head())
    # TO DO: display the most common month
    if month.lower() == 'all':
        # Only display the most common month when the month is not 
        # selected for the filter.
        month_group = df.groupby(['Month'])['Start Time'].count()
        month_name = month_list[month_group.idxmax()]
        month_records = '({} trips)'.format(month_group.max())
        title = 'Most Common Month'
        print(
            f'{title: <22}{month_name.title(): <12}{month_records: >10}'
        )

    else:
        print('Cannot calculate Most Common Month as only {} '.format(
            month.title()) + 'selected in filter.')

    # Display the most common day of week and the number of trips for 
    # the filtered data.
    if day.lower() == 'all':
        # Only display the most common day when the day is not selected
        # for the filter.
        day_group = df.groupby(['day_of_week'])['Start Time'].count()
        day_name = day_group.idxmax()
        max_day = '({} trips)'.format(day_group.max())
        title = 'Most Common Day'
        print(f'{title: <22}{day_name.title(): <12}{max_day: >10}')
    else:
        print('Cannot calculate Most Common Day as only {} '.format(
            day.title()) + 'selected in filter.')
    # TO DO: display the most common start hour
    df_time = df
    df_time['Start Hour'] = df_time['Start Time'].dt.hour
    time_group = df_time.groupby(['Start Hour'])['Start Time'].count()
    hour_trips = '({} trips)'.format(time_group.max())                                
    title = 'Most Common Hour'
    print(
        f'{title: <22}{time_group.idxmax(): <12}{hour_trips: >10}'
    )

    print("\nCalculation of Time Statistics took %s seconds." % (
        time.time() - start_time))


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
        
    Arguments:
        df - pandas dataframe - contains the filtered ride share data for the
             selected city.
    """

    print('-'*43)
    print('MOST POPULAR STATION AND TRIP STATISTICS:')
    print('-'*43)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station_group = df.groupby(
        ['Start Station'])['Start Time'].count()
    max_start_station_name = start_station_group.idxmax()
    max_start_station_records = start_station_group.max()
    print('Most Commonly used Start Station\t= {}\t({} trips)'.format(
        max_start_station_name.title(), max_start_station_records))

    # Display most commonly used end station
    end_station_group = df.groupby(['End Station'])['Start Time'].count()
    max_end_station_name = end_station_group.idxmax()
    max_end_station_records = end_station_group.max()
    print('Most Commonly used End Station\t= {}\t({} trips)'.format(
        max_end_station_name.title(), 
        max_end_station_records))

    # Display most frequent combination of start station and end station
    # trip
    trip_df = df
    trip_df['Trip Name'] = ('Start Station\t\t\t= ' + trip_df['Start Station']
                            + '\nEnd Station\t\t\t= ' + trip_df['End Station'])
    trip_group = trip_df.groupby(['Trip Name'])['Start Time'].count()
    max_trip_name = trip_group.idxmax()
    max_trip_records = trip_group.max()
    print('\nMost Frequent Combination of Start Station and End Station:'
          + '\n{}\nTotal Trips:\t\t\t= {}'.format(max_trip_name.title(), 
                                      max_trip_records))

    print("\nCalculation of Most Popular Station and Trip Statistics took"
          + " %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

        Arguments:
        df - pandas dataframe - contains the filtered ride share data for the
             selected city.
    """

    print('-'*43)
    print('TRIP TRAVEL TIME STATISTICS:')
    print('-'*43)  
    print('\nCalculating Trip Travel Time Statistics...\n')
    
    start_time = time.time()

    # Display total travel time
    travel_time = round(df['Trip Duration'].sum()/60/60, 2)
    print('Total Travel time\t\t= {}'.format(travel_time)
         + ' hours')
    
    trip_duration_stats = df['Trip Duration'].describe() 
    trip_duration_stats = trip_duration_stats / 60
    trip_duration_stats = trip_duration_stats.round(decimals = 2)

    # Display mean travel time
    print('Mean (Average) Travel Time\t= {} minutes'.format(
        trip_duration_stats['mean']))
    
    # Display min and max travel times
    print('Minimum Travel Time\t\t= {} minutes'.format(
        trip_duration_stats['min']))
    print('Maximum Travel Time\t\t= {} minutes'.format(
        trip_duration_stats['max']))
    
    # Display additional statistical information
    print('\nAdditonal Statistical Information on the Travel Duration:\n')
    print('The Travel Time has a Standard Deviation of {} minutes'.format(
        trip_duration_stats['std']))

    print('Quartiles:\n\t25%\t'
          + '{} minutes\n\t50%\t{} minutes\n\t75%\t{}'.format(
              trip_duration_stats['25%'],
              trip_duration_stats['50%'],
              trip_duration_stats['75%']) + ' minutes')

    print("\nCalculation of Trip Travel Time Statistics took %s seconds."
        % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city_name):
    """Displays statistics on bikeshare users."""
    
    print('-'*43)
    print('USER TRIP STATISTICS:')
    print('-'*43)  
    print('\nCalculating Trip Travel Time Statistics...\n')
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Fix values that have NaN
    fix_nan = df.fillna('Not Selected')
    
    # Display counts of user types
    print('\nTrips by User Type\n' + '-'*43)
    user_group = fix_nan.groupby(['User Type'])['Start Time'].count()
    for group, value in user_group.items():
        print(f'{group: <15}{value: >20}')

    # Display counts of gender
    print('\nTrips by Gender Group\n' + '-'*43)
    if ('Gender' in fix_nan):
        
        gender_group = fix_nan.groupby(['Gender'])['Start Time'].count()
        for group, value in gender_group.items():
            print(f'{group: <15}{value: >20}')
    else:
        print('No Gender Information in {} data.'.format(
            city_name.title()))

    # TO DO: Display earliest, most recent and most common year of birth
    print('\nUser Birth Year Information\n' + '-'*43)

    if ('Birth Year' in df):
        birth_yr_stats = df['Birth Year'].describe()
        earliest_birth_yr = int(birth_yr_stats['min'])
        title = 'Earliest Birth Year'
        print(f'{title: <30}{earliest_birth_yr: >5}')
        most_recent_birth_yr = int(birth_yr_stats['max'])
        title = 'Most Recent Birth Year'
        print(f'{title: <30}{most_recent_birth_yr: >5}')
        # Most Common Year of Birth:
        birth_yr_group = df.groupby(['Birth Year'])['Start Time'].count()
        max_birth_yr_name = int(birth_yr_group.idxmax())
        max_birth_yr_rec = '(Total User Trips with {} birth year: {}*)'.format(
            max_birth_yr_name, birth_yr_group.max())
        #max_birth_yr_text = '(Total'
        title = 'Most Common User Birth Year' 
        print(f'{title: <30}{max_birth_yr_name: >5}')
        print(f'{max_birth_yr_rec}')
        print('* Count based on all trips in dataset, not grouped '
              + 'by individual users')

    else:
        print('No Birth Year Information in {} data.'.format(
            city_name.title()))

    print("\nCalculation of User Trip Statistics took %s seconds." 
          % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city_name, city_csv, month, day = get_filters()
        
        display_filter(city_name, month, day)
        continue_bikeshare = continue_to_stats()
        
        if continue_bikeshare == 'no':
            print('Exiting Bikeshare program.')
            break
        elif continue_bikeshare == 'restart':
            print('Restarting Bikeshare program.')
            continue
        else:
            df = load_data(city_csv, month, day)
            
            display_filter(city_name, month, day)
            general_info(df, city_name)
            
            display_filter(city_name, month, day)
            time_stats(df, month, day)

            # I added these 'program pauses' to allow the user to stop
            # and read each section on its own.
            program_pause = input('Hit Enter to see more statisitical ' 
                                  + 'information on the {}'.format(
                                      city_name.title())
                                  + ' Bikeshare data.')
            display_filter(city_name, month, day)
            station_stats(df)
            
            program_pause = input('Hit Enter to see more statisitical ' 
                                  + 'information on the {}'.format(
                                      city_name.title())
                                  + ' Bikeshare data.')
            display_filter(city_name, month, day)
            trip_duration_stats(df)
            
            program_pause = input('Hit Enter to see more statisitical '
                                  + 'information on the {}'.format(
                                      city_name.title())
                                  +' Bikeshare data.')
            display_filter(city_name, month, day)
            user_stats(df, city_name)

            # Check if user wants to run the program again.
            reloop = True
            while reloop:
                restart = input('\nWould you like to restart? '
                                + 'Enter (y)es or (n)o: ')
                # got sick of mis-typing yes so shortened to 'y'.
                try:
                    # Check that restart is not an empty string.
                    check_response = restart[0].lower()
                except:
                    print('Invalid entry, please try again.')
                    # Get another input if empty string.
                    continue
                else:
                    # Exit this loop if a string is received.
                    reloop = False
                    
            if restart[0].lower() != 'y':
                # End program if entered other than a word starting
                # with 'y'.
                break

if __name__ == "__main__":
	main()
