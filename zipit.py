import sys
import os
sys.path.append(os.environ['DATA_COLLECTOR_PATH'])
from common.utilities import get_logger, save_html_page, compress_file


for source_dir,  sub_dirs, files in os.walk(os.environ['NEWS_RAW_PATH'] + 'www.ccn.com/'):

    for file in files:
        path = source_dir + '/' + file
        path = path.replace('//','/')
        compress_file(path)

    #if(source_dir == '/home/arran/news/www.coindesk.com/page'):
    #    print(files)