import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter


def parse_leap_data(leap_file):
    # Import file
    data = pd.read_csv(leap_file)

    return data


def parse_glow_daily_feeding_data(glow_file):
    # Import file
    data = pd.read_csv(glow_file)

    # Convert date column to datetime
    data['start_time_label'] = pd.to_datetime(
        data['start_time_label'], format='%Y/%m/%d %H:%M:%S')

    data_normalized = data['start_time_label'].dt.normalize()
    # Find first and last entry in column
    start_date = data['start_time_label'].iloc[-1].date()
    end_date = data['start_time_label'].iloc[0].date()

    # Final data
    data_list = []

    for current_date in pd.date_range(start_date, end_date):
        # print(single_date.strftime("%Y-%m-%d"))

        # Get all entires on this date
        date_key = data['start_time_label'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data[date_key]

        # Compute statistics
        sum_on_date = rows_on_date['bottle_ml'].sum()
        mean_on_date = rows_on_date['bottle_ml'].mean()
        max_on_date = rows_on_date['bottle_ml'].max()
        min_on_date = rows_on_date['bottle_ml'].min()
        sessions_on_date = rows_on_date['bottle_ml'].count()

        # Put stats in a list
        data_list.append([current_date, sum_on_date,
                          mean_on_date, min_on_date, max_on_date,
                          sessions_on_date])

    # Convert list to dataframe
    daily_data = pd.DataFrame(data_list, columns=[
        'date', 'sum', 'mean', 'min', 'max', 'sessions'])

    # daily_data.to_csv('glow_feeding_daily_stats.csv')

    return daily_data


def parse_hatch_data(hatch_file):
    # Import file
    data = pd.read_csv(hatch_file)

    # Keep date only, remove time
    hatch_dates = data['Start Time'].astype(str).str[0: 10]
    # Convert to datetime
    data['Start Time'] = pd.to_datetime(hatch_dates, format='%m/%d/%Y')
    # Sort and remove duplicates
    data = data.sort_values(by=['Start Time'], ascending=True)
    data = data.drop_duplicates(subset=['Start Time'], keep=False)

    return data


def parse_glow_weekly_data(glow_file):
    # Import file
    data = pd.read_csv(glow_file)

    # Convert string in "%h %m" to timedelta in hours
    columns_sleep = ['longest_sleep_avg', 'longest_sleep_max', 'longest_sleep_min',
                     'total_sleep_avg', 'total_sleep_max', 'total_sleep_min']

    for key in columns_sleep:
        data[key] = pd.to_timedelta(
            data[key]) / np.timedelta64(1, 'h')

    return data


def main():
    # Settings

    title_font_size = 10
    axis_font_size = 8
    alpha_value = 0.3

    sns.set(style="darkgrid")
    f, axarr = plt.subplots(2, 2)

    # Import data

    glow_weekly_data = parse_glow_weekly_data('data/glow_weekly.csv')
    glow_daily_feeding_data = parse_glow_daily_feeding_data(
        'data/glow_daily_feeding.csv')
    hatch_data = parse_hatch_data('data/hatch.csv')
    leap_data = parse_leap_data('data/leap_calendar.csv')

    # Chart 1 - Eat: Average Number of Feeding Sessions Per Day
    axarr[0, 0].plot(glow_daily_feeding_data['date'],
                     glow_daily_feeding_data['sessions'])
    axarr[0, 0].set_title('Eat: Number of Feeding Sessions',
                          fontsize=title_font_size)
    axarr[0, 0].set_xlabel('Time (Weeks)', fontsize=axis_font_size)
    axarr[0, 0].set_ylabel('Number of Feeding Sessions',
                           fontsize=axis_font_size)
    axarr[0, 0].tick_params(labelsize=axis_font_size)
    axarr[0, 0].set_xticks(axarr[0, 0].get_xticks()[::2])

    # Chart 2 - Eat: Daily, Average Consumed Per Day(mL)
    axarr[0, 1].plot(glow_daily_feeding_data['date'],
                     glow_daily_feeding_data['sum'])
    axarr[0, 1].set_title('Eat: Daily Total (mL)',
                          fontsize=title_font_size)
    axarr[0, 1].set_xlabel('Date', fontsize=axis_font_size)
    axarr[0, 1].set_ylabel('Daily Total (mL)', fontsize=axis_font_size)
    axarr[0, 1].tick_params(labelsize=axis_font_size)
    axarr[0, 1].set_xticks(axarr[0, 1].get_xticks()[::2])

    # Chart 3 - Eat: Daily, Average Consumed Per Day(mL)
    axarr[1, 0].plot(glow_daily_feeding_data['date'],
                     glow_daily_feeding_data['mean'])
    axarr[1, 0].set_title('Average Volume Per Session (mL)',
                          fontsize=title_font_size)
    axarr[1, 0].set_xlabel('Date', fontsize=axis_font_size)
    axarr[1, 0].set_ylabel(
        'Average Volume Per Session (mL)', fontsize=axis_font_size)
    axarr[1, 0].tick_params(labelsize=axis_font_size)
    axarr[1, 0].set_xticks(axarr[1, 0].get_xticks()[::2])

    # Export

    f.subplots_adjust(wspace=0.35, hspace=0.5)
    f.set_size_inches(16, 8.5)
    f.savefig("Baby_Stats_daily.pdf", bbox_inches='tight')
    f.clf()


main()
