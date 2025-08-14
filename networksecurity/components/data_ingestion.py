from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

## configuration of the Data Ingestion Config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pandas as pd
from typing import List
import pymongo
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
     def __init__(self, data_ingestion_config: DataIngestionConfig):
          try:
               self.data_ingestion_config = data_ingestion_config
          except Exception as e:
               raise NetworkSecurityException(e, sys)
     
     def export_collection_as_dataframe(self) -> List[dict]:
          """
          Read data from MongoDB collection and return as a DataFrame.
          """
          try:
               database_name = self.data_ingestion_config.database_name
               collection_name = self.data_ingestion_config.collection_name
               self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
               collection= self.mongo_client[database_name][collection_name] 
               df=pd.DataFrame(list(collection.find()))
               if "_id" in df.columns.to_list():
                    df=df.drop(columns=["_id"], axis=1)
               
               df.replace({"na": np.nan}, inplace=True)
               return df
                    
          except Exception as e:
               raise NetworkSecurityException(e, sys)
          
     def export_data_into_feature_store(self, dataframe: pd.DataFrame):
          """
          Save the DataFrame to the feature store file path.
          """
          try:
               feature_store_file_path = self.data_ingestion_config.feature_store_file_path
               #creating folder if not exists
               dir_path = os.path.dirname(feature_store_file_path)
               os.makedirs(dir_path, exist_ok=True)    
               #exporting dataframe to csv
               dataframe.to_csv(feature_store_file_path, index=False, header=True)
               return dataframe
          except Exception as e:
               raise NetworkSecurityException(e, sys)
     
     def split_data_as_train_test(self, dataframe: pd.DataFrame) -> List[pd.DataFrame]:
          """
          Split the DataFrame into training and testing sets.
          """
          try:
               train_set, test_set = train_test_split(
                    dataframe, 
                    test_size=self.data_ingestion_config.train_test_split_ratio
               )
               logging.info(f"Train set shape: {train_set.shape}, Test set shape: {test_set.shape}")
               logging.info("Exporting train and test sets to respective file paths.")
               # Save the train and test sets to their respective file paths
               dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
               os.makedirs(dir_path, exist_ok=True)
               
               logging.info("Exporting train set to file path.")
               train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
               logging.info("Exported test set to file path.")
               test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
               
               
          except Exception as e:
               raise NetworkSecurityException(e, sys)
     
     def initiate_data_ingestion(self):
          try:
               dataframe = self.export_collection_as_dataframe()
               dataframe = self.export_data_into_feature_store(dataframe)
               self.split_data_as_train_test(dataframe)
               dataingestionartifact = DataIngestionArtifact(
                    train_file_path=self.data_ingestion_config.training_file_path,
                    test_file_path=self.data_ingestion_config.testing_file_path
               )
               logging.info("Data ingestion completed successfully.")
               return dataingestionartifact
          except Exception as e:
               raise NetworkSecurityException(e, sys) 