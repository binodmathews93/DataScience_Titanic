#-*- coding:utf-8 -*-

import os
from dotenv import load_dotenv, find_dotenv
from requests import session
import logging

# payload for login to kaggle

payload = {
    '__RequestVerificationToken': '',
    'username': os.environ.get("KAGGLE_USERNAME"),
    'password': os.environ.get("KAGGLE_PASSWORD"),
    'rememberme': 'false'
}

def extract_data(url, file_path):
    '''
    extract data from kaggle
    
    '''
    print('extracting data from %s',file_path)
    # setup session
    with session() as c:
        
        # post request
        loginurl = 'https://www.kaggle.com/account/login'
        response = c.get(loginurl).text
        AFToken = response[response.index('antiForgeryToken')+19:response.index('isAnonymous: ')-12]
        print("AntiForgeryToken={}".format(AFToken))
        payload['__RequestVerificationToken']=AFToken
        c.post(loginurl + "?isModal=true&returnUrl=/", data=payload)
    
        # open file to write
        with open(file_path, 'w') as handler:
            response = c.get(url, stream=True)
            for block in response.iter_content(1024):
                handler.write(block)
                
def main(project_dir):
    '''
    main method
    
    '''
    print('main method')
    #get logger
    logger = logging.getLogger(__name__)
    logger.info("getting raw data")
    
    # urls
    train_url = 'https://www.kaggle.com/c/titanic/download/train.csv'
    test_url = 'https://www.kaggle.com/c/titanic/download/test.csv'
    
    # file paths
    raw_data_path = os.path.join(os.path.pardir,'data','raw')
    train_data_path = os.path.join(raw_data_path,'train.csv')
    test_data_path = os.path.join(raw_data_path,'test.csv')
    
    # extract data
    extract_data(train_url,train_data_path)
    extract_data(test_url,test_data_path)
    logger.info("Downloaded raw training and test data")
    
if __name__ == '__main__':
    # getting root directory
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    # setup logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    
    # find .env automatically by walking up directories till its found
    dotenv_path = find_dotenv()
    
    # load up the entries as environmental variables
    load_dotenv(dotenv_path)
    
    # call the main
    main(project_dir)
    