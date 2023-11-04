import pandas as pd
import datetime as dt
import boto3
import os
from datetime import date, datetime
from newsapi import NewsApiClient

# Conver the date format
def convert_date_format(date_string):
    datetime_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date

# Function to clean dataframe before sending it to s3
def clean_data(df):
    # Data Preparation
    df['sourceName'] = df['source'].apply(lambda x: pd.Series({'source_name': x.get('name')}))
    df.drop('source', axis=1, inplace=True)
    df['publishedAt'] = df['publishedAt'].apply(convert_date_format)
    df['snapshotDate'] = date.today()
    df = df[['title', 'description', 'url', 'author', 'sourceName', 'category', 'country','urlToImage',
       'content','publishedAt', 'snapshotDate']]
    
    return df

# Define paths and send df to S3
def send_to_s3(df):
    # Name of the file
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    currentWeek = dt.datetime.now().isocalendar()[1]

    # Define your S3 bucket and file path
    bucket_name = 'bucket-by-tf'
    folder_name = 'newsapi_raw_{}_w{}'.format(currentYear, currentWeek)
    file_name = 'newsapi_raw_{}_w{}_{}.csv'.format(currentYear, currentWeek, currentDay)
    file_key = f'inputs/{folder_name}/{file_name}'

    # Upload CSV file to S3
    s3 = boto3.client('s3')
    s3.put_object(Body=df, Bucket=bucket_name, Key=file_key)


def lambda_handler(event, context):
    categories = ['business', 'entertainment', 'technology',  'general', 'health', 'science', 'sports']
    countries = ['us', 'gb']
    
    # Init
    api_key_value = os.environ.get('api_key')
    newsapi = NewsApiClient(api_key=api_key_value)
    
    dfs = []

    for n in range(len(categories)):
        for i in range(len(countries)):
            raw_dataframe = newsapi.get_top_headlines(
                                          category=categories[n],
                                          country=countries[i])
        
            # create a DataFrame from the dictionary
            raw_dataframe = pd.DataFrame(raw_dataframe['articles'])
    
            # add information about category and country
            raw_dataframe['category'] = categories[n]
            raw_dataframe['country'] = countries[i]
         
            dfs.append(raw_dataframe)
        
    # Concat dataframes and clean data 
    result_df = clean_data(pd.concat(dfs))

    # Convert DataFrame to CSV
    csv_data = result_df.to_csv(index=False)

    # Assign correct paths and send the csv data to S3
    send_to_s3(csv_data)

    return {
        'statusCode': 200,
        'body': f'CSV file saved'
    }
