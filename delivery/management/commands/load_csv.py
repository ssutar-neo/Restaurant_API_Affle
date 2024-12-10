# import pandas as pd 
# from django.core.management.base import BaseCommand
# import os
# import datetime
# import shutil
# import numpy as np
# import requests
# import sqlite3


# class Command(BaseCommand):
#     help = "Load data from csv"

#     def handle(self, *args, **kwargs):
#         input_file_url = 'https://s3.amazonaws.com/test.jampp.com/dmarasca/takehome.csv'
#         csv_file_path = r"downloads/takehome.csv"

#         response = requests.get(input_file_url, stream=True)
#         if response.status_code == 200:
#             if os.path.exists(csv_file_path):
#                 print(f"Old file detected at {csv_file_path}. Deleting it...")
#                 os.remove(csv_file_path)

#             with open(csv_file_path, 'wb') as f:
#                 f.write(response.content)
#             print(f"New file downloaded and saved to {csv_file_path}.")
#         else:
#             print(f"Failed to fetch the file. Status code: {response.status_code}")
#             return

#         data = pd.read_csv(csv_file_path)
#         data = data.replace({pd.NA: None, pd.NaT: None, np.nan: None})

#         connection = sqlite3.connect('db.sqlite3')  
#         cursor = connection.cursor()

#         cursor.execute("DELETE FROM delivery_restaurant")  

#         for _, row in data.iterrows():
#             cursor.execute(
#                 """
#                 INSERT INTO delivery_restaurant (id, latitude, longitude, availability_radius, open_hour, close_hour, rating)
#                 VALUES (?, ?, ?, ?, ?, ?, ?)
#                 """, 
#                 (row['id'], row['latitude'], row['longitude'], row['availability_radius'], row['open_hour'], row['close_hour'], row['rating'])
#             )

#         connection.commit()
#         print("Data loaded successfully")

#         # Archive the CSV file
#         archive_dir = 'archive/'
#         os.makedirs(archive_dir, exist_ok=True)
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         archive_path = os.path.join(archive_dir, f"restaurant_{timestamp}.csv")
#         shutil.move(csv_file_path, archive_path)

#         print("File archived successfully")


import pandas as pd
from django.core.management.base import BaseCommand
import os
import datetime
import shutil
from sqlalchemy import create_engine,text
import sqlite3
import requests

class Command(BaseCommand):
    help = "Load data from CSV into the SQLite database using pandas to_sql"

    def handle(self, *args, **kwargs):
        input_file_url = 'https://s3.amazonaws.com/test.jampp.com/dmarasca/takehome.csv'
        csv_file_path = r"downloads/takehome.csv"

        response = requests.get(input_file_url, stream=True)
        if response.status_code == 200:
            if os.path.exists(csv_file_path):
                print(f"Old file detected at {csv_file_path}. Deleting it...")
                os.remove(csv_file_path)

            with open(csv_file_path, 'wb') as f:
                f.write(response.content)
            print(f"New file downloaded and saved to {csv_file_path}.")
        else:
            print(f"Failed to fetch the file. Status code: {response.status_code}")
            return

        data = pd.read_csv(csv_file_path)
        data = data.replace({pd.NA: None})

        sqlite_db_path = "db.sqlite3"  
        engine = create_engine(f"sqlite:///{sqlite_db_path}")

        with engine.connect() as connection:
            connection.execute(text("DELETE FROM delivery_restaurant"))
            connection.commit()

        with engine.connect() as connection:    
            data.to_sql(
                name='delivery_restaurant',  
                con=engine, 
                if_exists='append', 
                index=False 
            )

        with engine.connect() as connection:
            result = connection.execute(text("Select count(*) as cnt FROM delivery_restaurant"))
            print(result.fetchone())

        print(f"Data loaded successfully. Total records inserted: {len(data)}")

        archive_dir = 'archive/'
        os.makedirs(archive_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = os.path.join(archive_dir, f"restaurant_{timestamp}.csv")
        shutil.move(csv_file_path, archive_path)

        print(f"File archived successfully to {archive_path}")
