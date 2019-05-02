import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.ticker import MaxNLocator


def format_plot(date_data, plot_object):
    axis_font_size = 8

    plot_object.set_xlim(date_data.iloc[0],
                         date_data.iloc[-1])
    plot_object.tick_params(labelsize=axis_font_size)
    plot_object.set_xticks(plot_object.get_xticks()[::2])
    plot_object.xaxis.set_major_locator(
        MonthLocator(range(1, 13), bymonthday=1, interval=1))
    plot_object.xaxis.set_major_formatter(DateFormatter("%Y/%m"))


def convert_date(data):
    # Convert date column to datetime
    data['start_time_label'] = pd.to_datetime(
        data['start_time_label'], format='%Y/%m/%d %H:%M:%S')
    data['end_time_label'] = pd.to_datetime(
        data['end_time_label'], format='%Y/%m/%d %H:%M:%S')

    # Find first and last entry in column
    start_date = data['start_time_label'].iloc[-1].date()
    end_date = data['start_time_label'].iloc[0].date()

    return data, start_date, end_date


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


def parse_glow_daily_diaper_sleep_data(glow_file):
    # Import file
    data = pd.read_csv(glow_file)

    # Convert the date info
    data, start_date, end_date = convert_date(data)

    # Separate sleep and diaper data
    data_sleep = data.loc[data['key'] == "sleep"]
    data_diaper = data.loc[data['key'] == "diaper"]

    # Final data
    diaper_data_list = []
    sleep_data_list = []

    # Diaper
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data_diaper['start_time_label'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data_diaper[date_key]

        # Compute total diaper count
        total_diaper_count = rows_on_date['val'].count()

        # Separate pees and poops
        total_pee_count = 0
        total_poop_count = 0
        for index, diaper_event in rows_on_date.iterrows():
            key = diaper_event['val']
            if (key == '65536'):  # Pee only
                total_pee_count += 1
            else:
                total_pee_count += 1
                total_poop_count += 1
            # todo, not catching poop only cases (a few of them)

        # Put stats in a list
        diaper_data_list.append(
            [current_date, total_diaper_count, total_pee_count, total_poop_count])

    # Sleep
    offset = 0

    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data_sleep['start_time_label'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data_sleep[date_key]

        # Compute number of nap sessions
        nap_sessions_on_date = 0

        for index, sleep_session in rows_on_date.iterrows():
            timestamp = sleep_session['start_time_label']
            time7am = timestamp.replace(
                hour=7, minute=0, second=0, microsecond=0)
            time7pm = timestamp.replace(
                hour=19, minute=0, second=0, microsecond=0)
            if (timestamp > time7am) and (timestamp < time7pm):
                nap_sessions_on_date += 1

        # Total sleep

        # Get duration for each row, then sum
        elapsed_time = rows_on_date['end_time_label'] - \
            rows_on_date['start_time_label']
        total_sleep_duration = elapsed_time.sum().total_seconds()

        # Add offset from previous day
        total_sleep_duration += offset

        # Get the first row in the block
        start_last = rows_on_date['start_time_label'].iloc[0]
        end_last = rows_on_date['end_time_label'].iloc[0]

        # Catch session that extend past midnight
        if(end_last.date() > start_last.date()):  # if extends to next day
            midnight = end_last.replace(
                hour=0, minute=0, second=0, microsecond=0)

            # Subtract duration from today's total
            offset = (end_last - midnight).total_seconds()
            total_sleep_duration -= offset
            # Keep the offset to add to tomorrow's total

        # Convert to hours
        total_sleep_duration = total_sleep_duration // 3600

        # Longest session
        longest_session = elapsed_time.max().total_seconds() // 3600

        # Put stats in a list
        sleep_data_list.append(
            [current_date, nap_sessions_on_date, total_sleep_duration, longest_session])

    # Convert list to dataframe
    daily_diaper_data = pd.DataFrame(
        diaper_data_list, columns=['date', 'total_diaper_count', 'pee_count', 'poop_count'])
    daily_sleep_data = pd.DataFrame(
        sleep_data_list, columns=['date', 'total_naps', 'total_sleep_duration', 'longest_session'])

    return daily_diaper_data, daily_sleep_data


def parse_glow_daily_feeding_data(glow_file):
    # Import file
    data = pd.read_csv(glow_file)

    # Convert the date info
    data, start_date, end_date = convert_date(data)

    # Final data
    feeding_data_list = []

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
        feeding_data_list.append([current_date, sum_on_date,
                                  mean_on_date, min_on_date, max_on_date,
                                  sessions_on_date])

    # Convert list to dataframe
    daily_feeding_data = pd.DataFrame(feeding_data_list, columns=[
        'date', 'sum', 'mean', 'min', 'max', 'sessions'])

    return daily_feeding_data


def main():
    # Settings

    title_font_size = 10
    axis_font_size = 8
    alpha_value = 0.3

    sns.set(style="darkgrid")
    f, axarr = plt.subplots(3, 3)

    # Import data

    glow_daily_feeding_data = parse_glow_daily_feeding_data(
        'data/glow_daily_feeding.csv')
    daily_diaper_data, daily_sleep_data = parse_glow_daily_diaper_sleep_data(
        'data/glow_sleep_diaper_sleep.csv')
    hatch_data = parse_hatch_data('data/hatch.csv')

    # Chart 1 - Eat: Daily, Average Consumed Per Day(mL)
    axarr[0, 0].plot(glow_daily_feeding_data['date'],
                     glow_daily_feeding_data['mean'])
    axarr[0, 0].fill_between(
        glow_daily_feeding_data['date'].values, glow_daily_feeding_data['mean'],
        glow_daily_feeding_data['max'], alpha=alpha_value)
    axarr[0, 0].fill_between(
        glow_daily_feeding_data['date'].values, glow_daily_feeding_data['mean'],
        glow_daily_feeding_data['min'], alpha=alpha_value)
    axarr[0, 0].set_title('Eat: Daily Volume Per Session (mL)',
                          fontsize=title_font_size)
    axarr[0, 0].set_xlabel('Date', fontsize=axis_font_size)
    axarr[0, 0].set_ylabel(
        'Average Volume Per Session (mL)', fontsize=axis_font_size)
    axarr[0, 0].yaxis.set_ticks(np.arange(0, 240, 30))
    format_plot(glow_daily_feeding_data['date'], axarr[0, 0])

    # Chart 2 - Eat: Number of Feeding Sessions Per Day
    axarr[0, 1].plot(glow_daily_feeding_data['date'],
                     glow_daily_feeding_data['sessions'])
    axarr[0, 1].set_title('Eat: Number of Feeding Sessions',
                          fontsize=title_font_size)
    axarr[0, 1].set_xlabel('Time', fontsize=axis_font_size)
    axarr[0, 1].set_ylabel('Number of Feeding Sessions',
                           fontsize=axis_font_size)
    axarr[0, 1].yaxis.set_ticks(np.arange(4, 13, 2))
    format_plot(glow_daily_feeding_data['date'], axarr[0, 1])

    # Chart 3 - Eat: Daily, Daily Total Volume (mL)
    axarr[0, 2].plot(glow_daily_feeding_data['date'],
                     glow_daily_feeding_data['sum'])
    axarr[0, 2].set_title('Eat: Daily Total Volume (mL)',
                          fontsize=title_font_size)
    axarr[0, 2].set_xlabel('Date', fontsize=axis_font_size)
    axarr[0, 2].set_ylabel('Daily Total (mL)', fontsize=axis_font_size)
    format_plot(glow_daily_feeding_data['date'], axarr[0, 2])

    # Chart 4 - Sleep: Total Naps (7:00-19:00)
    axarr[1, 0].plot(daily_sleep_data['date'],
                     daily_sleep_data['total_naps'])
    axarr[1, 0].set_title('Sleep: Total Naps (7:00-19:00)',
                          fontsize=title_font_size)
    axarr[1, 0].set_xlabel('Date', fontsize=axis_font_size)
    axarr[1, 0].set_ylabel(
        'Total Naps', fontsize=axis_font_size)
    format_plot(daily_sleep_data['date'], axarr[1, 0])

    # Chart 5 - Sleep: Longest Duration of Uninterrupted Sleep (Hours)
    axarr[1, 1].plot(daily_sleep_data['date'],
                     daily_sleep_data['longest_session'])
    axarr[1, 1].set_title('Sleep: Longest Sleep Duration (Hr)',
                          fontsize=title_font_size)
    axarr[1, 1].set_xlabel('Date', fontsize=axis_font_size)
    axarr[1, 1].set_ylabel(
        'Longest Sleep Duration (Hr)', fontsize=axis_font_size)
    axarr[1, 1].yaxis.set_ticks(np.arange(0, 9, 1))
    format_plot(daily_sleep_data['date'], axarr[1, 1])

    # Chart 6 - Sleep: Total Sleep Per Day (Hours)
    axarr[1, 2].plot(daily_sleep_data['date'],
                     daily_sleep_data['total_sleep_duration'])
    axarr[1, 2].set_title('Sleep: Total Sleep (Hr)',
                          fontsize=title_font_size)
    axarr[1, 2].set_xlabel('Date', fontsize=axis_font_size)
    axarr[1, 2].set_ylabel(
        'Total Sleep (Hr)', fontsize=axis_font_size)
    axarr[1, 2].yaxis.set_ticks(np.arange(11, 21, 2))
    format_plot(daily_sleep_data['date'], axarr[1, 2])

    # Chart 7 - Diaper: Total Pees Per Day
    axarr[2, 0].plot(daily_diaper_data['date'],
                     daily_diaper_data['pee_count'])
    axarr[2, 0].set_title('Diaper: Total Pees',
                          fontsize=title_font_size)
    axarr[2, 0].set_xlabel('Date', fontsize=axis_font_size)
    axarr[2, 0].set_ylabel(
        'Total Pees', fontsize=axis_font_size)
    axarr[2, 0].yaxis.set_ticks(np.arange(4, 20, 2))
    format_plot(daily_diaper_data['date'], axarr[2, 0])

    # Chart 8 - Diaper: Total Poops Per Day
    axarr[2, 1].plot(daily_diaper_data['date'],
                     daily_diaper_data['poop_count'])
    axarr[2, 1].set_title('Diaper: Total Poops',
                          fontsize=title_font_size)
    axarr[2, 1].set_xlabel('Date', fontsize=axis_font_size)
    axarr[2, 1].set_ylabel(
        'Total Poops', fontsize=axis_font_size)
    axarr[2, 1].yaxis.set_ticks(np.arange(0, 10, 1))
    format_plot(daily_diaper_data['date'], axarr[2, 1])

    # Chart 9.a - Weight

    axarr[2, 2].plot(hatch_data['Start Time'], hatch_data['Amount'])
    axarr[2, 2].set_title('Weight (kg) / Percentile (%)',
                          fontsize=title_font_size)
    axarr[2, 2].set_xlabel('Date', fontsize=axis_font_size)
    axarr[2, 2].set_ylabel('Weight (kg)', fontsize=axis_font_size)
    axarr[2, 2].set_xlim(hatch_data['Start Time'].iloc[0],
                         hatch_data['Start Time'].iloc[-1])
    axarr[2, 2].tick_params(labelsize=axis_font_size)

    # Chart 9.b - Percentile

    axarr[2, 2] = axarr[2, 2].twinx()
    axarr[2, 2].plot(hatch_data['Start Time'],
                     hatch_data['Percentile'] * 100, 'r')
    axarr[2, 2].set_ylabel(
        'Percentile (%)', color='r', fontsize=axis_font_size)
    axarr[2, 2].set_xlim(hatch_data['Start Time'].iloc[0],
                         hatch_data['Start Time'].iloc[-1])
    axarr[2, 2].spines['right'].set_color('r')
    axarr[2, 2].yaxis.label.set_color('r')
    axarr[2, 2].tick_params(labelsize=axis_font_size, color='r')
    axarr[2, 2].xaxis.set_major_locator(
        MonthLocator(range(1, 13), bymonthday=1, interval=1))
    axarr[2, 2].xaxis.set_major_formatter(DateFormatter("%Y/%m"))

    # Export

    f.subplots_adjust(wspace=0.35, hspace=0.5)
    f.set_size_inches(16, 8.5)
    f.savefig("Baby_Stats_daily.pdf", bbox_inches='tight')
    f.clf()


main()
