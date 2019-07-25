### TODO automate last_id retrieval
import urllib.request
import time
import numpy as np
import os
from pathlib import Path

def download_files_from_urls_list(lastId=17529, urlsList, overwrite=True, urls_list='urls_list.txt')
    urls_list = []
    with open('urls_list.txt', 'r') as f:
        for i, line in enumerate(f):
            urls_list.appendline.rstrip().split()

    for i, item in enumerate(urlsList[lastId:]):
        fileNum = str(lastId+i)
        os.makedirs('listings/data/'+fileNum, exist_ok=overwrite)
        dl_path = 'listings/data/'+fileNum+ '/'
        if i%100 == 0:
            print(fileNum, item)
        for j, url in enumerate(item):
            file_name = str(j)+".jpg"
        try:
            urllib.request.urlretrieve(url, dl_path+file_name)
        except:
            # create error log
            error_file = 'errors.txt'
            with open(dl_path+error_file,"w+") as errors:
            errors.write(url+'\n')
            #       print('error in', folder, url)
        # Wait to download b/t 1 and 2 ms
        time_to_wait = np.random.uniform(low=.001, high=.002)

        time.sleep(time_to_wait)
