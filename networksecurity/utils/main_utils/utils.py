import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import numpy as np
import dill
import pickle


def read_yaml_file(file_path: str) -> dict:
     """Read a YAML file and return its content as a dictionary."""
     try:
          with open(file_path, 'rb') as yaml_file:
               return yaml.safe_load(yaml_file)
     except Exception as e:
          logging.error(f"Error reading YAML file at {file_path}: {e}")
          raise NetworkSecurityException(e, sys)
     
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
     """Write a dictionary to a YAML file."""
     try:
          if replace: 
               if os.path.exists(file_path):
                    os.remove(file_path)
          with open(file_path, 'w') as yaml_file:
               yaml.dump(content, yaml_file)
     except Exception as e:
          logging.error(f"Error writing YAML file at {file_path}: {e}")
          raise NetworkSecurityException(e, sys)
     
def save_numpy_array_data(file_path: str, array: np.array) -> None:
     """  Save a NumPy array to a file.
          file_path: str - Path to save the NumPy array.
          array: np.array - NumPy array to save.
     """
     try:
          dir_path = os.path.dirname(file_path)
          os.makedirs(dir_path, exist_ok=True)
          with open(file_path, 'wb') as file:
               np.save(file, array)
     except Exception as e:
          logging.error(f"Error saving NumPy array to {file_path}: {e}")
          raise NetworkSecurityException(e, sys)
     
def save_object(file_path: str, obj: object) -> None:
     """Save an object to a file using pickle."""
     try:
          logging.info(f"Saving object to {file_path}")
          dir_path = os.path.dirname(file_path)
          os.makedirs(dir_path, exist_ok=True)
          with open(file_path, 'wb') as file:
               pickle.dump(obj, file)
     except Exception as e:
          logging.info(f"Error saving object to {file_path}: {e}")
          raise NetworkSecurityException(e, sys)