from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT='-e .'

def get_requirements(file_path) -> List[str]:
    '''
    file_path:str : function expects its input (named file_path) to be a string. 
    List[str]: function will return a Python list, and each item in that list will be a string
    '''

    requirements = []

    with open(file_path) as file_obj:
        requirements=file_obj.readline()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

        return requirements
    
setup(
    name = 'VehicleLapsePrediction',
    version='0.0.1',
    author ='Mak',
    author_email = 'mohd.amilk09@gmail.com',
    packages=find_packages(),
    install_requirements=get_requirements('requirements.txt')
)