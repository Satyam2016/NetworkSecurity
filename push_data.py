import os
import sys
import json
import certifi

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca= certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

#creating ETL(extract, transform, load) pipeline for network data
#extracting data from csv file and loading it into mongodb

class NetworkDataExtract():
     def __inti__(self):
          try:
               pass
          except Exception as e:
               raise NetworkSecurityException(e, sys)
     
     def csv_to_json(self, file_path):
          try:
               data=pd.read_csv(file_path)
               data.reset_index(drop=True, inplace=True)
               records = list(json.loads(data.T.to_dict()).values())
               return records
          except Exception as e:
               raise NetworkSecurityException(e, sys)
     
     def insert_data_mongodb(self, records, database, collection):
          try:
               self.database = database
               self.collection = collection
               self.records = records
               
               self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
               self.database = self.mongo_client[self.database]
               self.collection = self.database[self.collection]
               self.collection.insert_many(self.records)
               return (len(self.records))
          except Exception as e:
               raise NetworkSecurityException(e, sys)
               
