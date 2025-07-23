from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    """
    This function will return the list of requirements
    """
    
    requirements_list :List[str] =[]
    try:
         with open('requirements.txt', 'r') as file:
               lines = file.readlines()
               for line in lines:
                    requirement=line.strip()
                    if requirement and requirement != '-e .':
                         requirements_list.append(requirement)
    except FileNotFoundError:
            print("requirements.txt file not found. Please ensure it exists.")
    return requirements_list


setup(
     name='NetworkSecurity',
     version='0.1',
     author="Satyam Kumar",
     author_email="sk9161511745@gmail.com",
     packages=find_packages(),
     install_requires=get_requirements()
)
                           