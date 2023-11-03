import json
import boto3
import pandas as pd
import re
import datetime as dt
from botocore.exceptions import ClientError
from io import StringIO


def get_current_week_key():
    # Name of the file
    currentYear = dt.datetime.now().year
    currentWeek = dt.datetime.now().isocalendar()[1]
    
    # Define your S3 bucket and file path
    folder_name = 'newsapi_raw_{}_w{}'.format(currentYear, currentWeek)
    folder_key = f'inputs/{folder_name}'
    
    return folder_key

def send_email(DF, SENDER, RECIPIENT):
    # Convert DataFrame to HTML table
    html_table = DF.to_html(classes='mystyle')
    
    # Define your SES configuration
    AWS_REGION = 'eu-central-1'
    SUBJECT = 'Weekly news'
    BODY_TEXT = 'Here is your DataFrame in the email body.'
    CHARSET = 'UTF-8'
    BODY_HTML = f"""<html>
    <head>
    <style>
    body {{
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    padding: 20px;
  }}
  .container {{
    max-width: 600px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  }}
  h1 {{
    color: #333333;
  }}
  .mystyle {{
    border-collapse: collapse;
    width: 100%;
  }}
  .mystyle th, td {{
    text-align: center;
    padding: 12px;
  }}
  .mystyle th {{
    background-color: #f2f2f2;
    color: #333333;
  }}
    </style>
    </head>
    <body>
  <h1 style="color:SlateGray;">Most important news from the last week.</h1>
  <table style="width:100%" border="1">
    {html_table}
    </body>
    </html>"""
    
    ses_client = boto3.client('ses', region_name = AWS_REGION)
    
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [RECIPIENT],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    
    
def lambda_handler(event, context):

    s3_client = boto3.client('s3')
    
    news_bucket = 'news-data-lake'
    news_key = get_current_week_key()
    
    # Fetch all the CSV files with the specified prefix from the S3 bucket
    file_list = []
    response = s3_client.list_objects_v2(Bucket=news_bucket, Prefix=news_key)
    
    for obj in response.get('Contents', []):
        key = obj['Key']
        if key.endswith('.csv'):
            file_list.append(key)
    
    # Initialize an empty dataframe to store the concatenated data
    concatenated_data = pd.DataFrame()

    # Read and concatenate the CSV files
    for file in file_list:
        obj = s3_client.get_object(Bucket=news_bucket, Key=file)
        df = pd.read_csv(obj['Body'])
        concatenated_data = pd.concat([concatenated_data, df], ignore_index=True)
    
    # Filter the DataFrame
    selected_words = ['iot', 'internet of things', 'industry', 
                    'sensors', 'cloud', 'aws', 'car', 'automotive']  # Search words
    selected_columns = ['title', 'description', 'content']   # Columns to check for selected words
    filtered_df = concatenated_data[concatenated_data[selected_columns].apply(lambda x: x.str.contains('|'.join(selected_words), case=False)).all(axis=1)]
    
    # Dropping rows with 'entertainment' and 'sport' in the 'category' column
    filtered_df = filtered_df[~filtered_df['category'].isin(['entertainment', 'sport'])]


    # Clean the DataFrame
    columns_to_drop = ['author', 'sourceName', 'urlToImage', 'content', 'description', 'snapshotDate','country']
    filtered_df = filtered_df.drop(columns_to_drop, axis = 1)
    # Renaming columns to start with upper case
    filtered_df.rename(columns=lambda x: x.capitalize(), inplace=True)

    # Send the dataframe via e-mail
    send_email(filtered_df, 'nikodem4799@gmail.com', 'niko.j.pietrzak@gmail.com')

    return {
        'statusCode': 200,
        'body': json.dumps('Email Sent Successfully.')
    }