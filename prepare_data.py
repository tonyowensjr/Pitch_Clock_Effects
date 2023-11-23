from constants import SAVANT_URL,TIMING_COLS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import argparse
import pandas as pd
import re


def prepare_timing(table_info: list) -> pd.DataFrame:
    """Take in a list of strings from the Baseball Savant table and convert it into a dataframe

    Args:
        table_info (list): The list of strings from the Baseball Savant table

    Returns:
        pd.DataFrame: The output dataframe
    """
    # get the pitcher names and their stats
    names = [re.split(r'\d',' '.join(x.split(' ')[1:]))[0].rstrip() for x in table_info[4:]]
    stats = [re.split(r"[aA-zZ.é][ ]{1}(?=\d)",x)[1].split(' ')[:-1] for x in table_info[4:]]

    # create the dataframe
    game_data = pd.DataFrame(stats,columns = TIMING_COLS)
    game_data.insert(0,'pitcher_name',names)
    game_data.insert(1,'timing_name',game_data.pitcher_name.apply(lambda x:x.split(', ')[-1] +' ' + x.split(', ')[0]))

    return game_data

def prepare_player_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the player data dataframe

    Args:
        df (pd.DataFrame): The raw player data dataframe

    Returns:
        pd.DataFrame: The cleaned player data dataframe
    """

    # clean the name column by removing unwanted characters
    df.Name = df.Name.apply(lambda x:x.replace('*','').replace('\xa0',' '))

    return df

def merge_player_data(df1: pd.DataFrame,year1:str,df2: pd.DataFrame,year2:str) -> pd.DataFrame:
    """Merge the pitcher data from the given years and return the merged dataframe

    Args:
        df1 (pd.DataFrame): The pitcher data dataframe for the first year
        df2 (pd.DataFrame): The pitcher data dataframe for the second year

    Returns:
        pd.DataFrame: The merged dataframe
    """

    # process both dataframes
    df1,df2 = prepare_player_data(df1),prepare_player_data(df2)

    # merge the dataframes
    merged_data = df1.add_suffix(f'_{year1}').merge(df2.add_suffix(f'_{year2}'),
                                                    left_on=f'Name-additional_{year1}',
                                                    right_on=f'Name-additional_{year2}',how='inner')

    # return the merged dataframe
    return merged_data


def timing_data() -> pd.DataFrame:
    """Acquire the Pitch Tempo data from Baseball Savant for a given year

    Returns:
        pd.DataFrame: A dataframe containing the Pitch Tempo data for the given year
    """

    # create the argument parser
    parser = argparse.ArgumentParser(description='Get the Pitch Tempo data from Baseball Savant')

    # define the argument for the year to get the data from
    parser.add_argument('--year',help='The year to acquire the data for',default='2022',type=str,required=False)


    # define the argument for the game type for the data
    parser.add_argument('--game_type',help='Flag to denote acquiring data from regular season games "Regualr"\
                        playoff games "Playoff" or both "All"',default='Regular',type=str,required=False)


    # parse the arguments
    year = parser.parse_args().year
    game_type = parser.parse_args().game_type

    # format the Baseball Savant URL
    url = SAVANT_URL.format(game_type=game_type,year=year)

    # create the web driver and go to the URL
    wd = webdriver.Chrome()
    wd.get(url)

    # define the locator for the table
    table_locator = (By.ID, "pitcher_tempo_table")

    # Wait for the text of the table to populate
    WebDriverWait(wd, 10).until(
        lambda driver: driver.find_element(*table_locator).text != ""
    )

    # get the text of the table
    table_info = wd.find_element(By.ID,'pitcher_tempo_table').text.split('\n')
    wd.close()

    # create the dataframe
    df = prepare_timing(table_info)

    # save the datafrmae to the data file
    df.to_csv(f'data/timing_data_{game_type.lower()}_{year}.csv',index=False)

    # return the dataframe
    return df

if __name__ == '__main__':
    timing_data()

