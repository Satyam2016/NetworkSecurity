import yaml
from networksecurity.exception.exception import NetworkSecurityException
import networksecurity.logging.logger as logging
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