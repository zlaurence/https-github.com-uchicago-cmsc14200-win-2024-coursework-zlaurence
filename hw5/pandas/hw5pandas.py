import pandas as pd


def load_divvy_data() -> pd.DataFrame:
    """
    Load Dataframe containing ride data from Divvy Bikes for 2023

    Returns:
        pd.DataFrame: Divvy data
    """
    return pd.read_csv("data/divvy_2023_sample_10k.csv")


def load_weather_data() -> pd.DataFrame:
    """
    Load Dataframe containing weather data for Chicago area for 2023

    Returns:
        pd.DataFrame: Weather data
    """
    return pd.read_csv("data/weather_chicago_2023.csv")


def summarize_ride_by_date(divvy_df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize Divvy ride data by date. Aggregates ride count and average
    ride duration by date.
    Args:
        divvy_df (pd.DataFrame): Divvy ride data
    Returns:
        pd.DataFrame: Summary of ride data by date. Resulting dataframe
         contains the following index and columns:
            - ride_date: Date of the ride
            - ride_count: Number of rides on that date
    """
    divvy_df['started_at'] = pd.to_datetime(divvy_df['started_at'])
    divvy_df['ride_date'] = divvy_df['started_at'].dt.date.astype(str)
    summary_df = divvy_df.groupby('ride_date').size().reset_index(name='ride_count')
    
    return summary_df



def merge_rides_and_weather(
    divvy_summary: pd.DataFrame, weather_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge Divvy ride data with chicago weather data by date

    Args:
        divvy_summary (pd.DataFrame): Summary of ride data by date
        weather_data (pd.DataFrame): Weather data
    Returns:
        pd.DataFrame: Merged data
                Resulting dataframe is indexed by ride_date, and contains the
                following columns:
                - ride_count: Number of rides on that date
                - temp_max: Maximum temperature on that date
                - temp_min: Minimum temperature on that date
                - temp_avg: Average temperature on that date
                - temp_departure: Departure from normal temperature on that date

    """
    if divvy_summary.index.name != 'ride_date':
        divvy_summary.set_index('ride_date', inplace=True)
    if weather_data.index.name != 'ride_date':
        weather_data = weather_data.rename(columns={'calendar_date': 'ride_date'}).set_index('ride_date')
    merged_data = divvy_summary.join(weather_data, how='outer')
    expected_columns = ['ride_count', 'temp_max', 'temp_min', 'temp_avg', 'temp_departure']
    merged_data = merged_data[expected_columns]

    return merged_data


def compute_correlation(
    merged_data: pd.DataFrame, variable1: str, variable2: str
) -> float:
    """
    Compute the correlation between two variables in the dataframe

    Args:
        merged_data (pd.DataFrame): Merged data
        variable1 (str): Name of the first variable
        variable2 (str): Name of the second variable

    Returns:
        float: Correlation between the two variables
    """
    correlation = merged_data[variable1].corr(merged_data[variable2])
    return correlation


# Bonus Plotting
def plot_visual_correlation(
    merged_data: pd.DataFrame, variable1: str, variable2: str
) -> None:
    """
    Plot the correlation between two variables in the dataframe

    Args:
        merged_data (pd.DataFrame): Merged data
        variable1 (str): Name of the first variable
        variable2 (str): Name of the second variable
    """
    ax = merged_data.plot(y=variable1)
    merged_data.plot(y=variable2, secondary_y=True, ax=ax, rot=90)
