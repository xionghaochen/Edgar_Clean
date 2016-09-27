# !/usr/bin/env python
# -*- coding:utf-8 -*-

'The second part of edgar'

__author__='Walter Xiong'

import os
import shutil
import sys
from bs4 import BeautifulSoup

# Create a CLEANED directory
def main():

    for dirpath,dirnames,filenames in os.walk(os.path.abspath('.')):

        for filename in filenames:

            if os.path.splitext(filename)[1] == '.idx':

                if os.path.splitext(filename)[0] in dirnames:

                    original_dir = os.path.join(os.path.abspath('.'),os.path.splitext(filename)[0])
                    cleaned_dir = os.path.join(os.path.abspath('.'), os.path.splitext(filename)[0] + '_CLEANED')

                    if os.path.isdir(cleaned_dir):
                        shutil.rmtree(cleaned_dir)

                    if not os.path.isdir(cleaned_dir):
                        os.mkdir(cleaned_dir)

                else:
                    sys.exit('Error: Original directory %r cannot be found' % os.path.splitext(filename)[0])

    traverse_folders(original_dir,cleaned_dir)

# Find the .htm files
def traverse_folders(original_dir,cleaned_dir):

    original_folders = os.listdir(original_dir)

    count = 0

    for f in original_folders:

        if f == 'ConnError.txt' or f == 'IOError.txt' or f == 'Not_Found.txt' or f == '.DS_Store'or os.path.splitext(f)[1].lower() == '.swp':
            continue

        if os.path.splitext(f)[1].lower() == '.pdf' or os.path.splitext(f)[1].lower() == '.xml' or os.path.splitext(f)[1].lower() == '.paper' or os.path.splitext(f)[1].lower() == '.txt':
            shutil.copy(os.path.join(original_dir,f),cleaned_dir)
            continue

        if os.path.splitext(f)[1].lower() == '.htm' :
            count = count + 1
            print f
            print str(count) + ' of ' + str(len(original_folders)) + ' files\n'

            clean_htm_file(original_dir,cleaned_dir,f)

        else:
            print 'Processing ' + f + ' ...\n'

            if not os.path.isdir(os.path.join(cleaned_dir,f)):
                os.mkdir(os.path.join(cleaned_dir,f))
                # os.mkdir(os.path.join(os.path.join(cleaned_dir,f), 'Manual_Clean'))

            traverse_folders(os.path.join(original_dir,f),os.path.join(cleaned_dir,f))


def clean_htm_file(original_dir,cleaned_dir,file):

    original_content = open(os.path.join(original_dir,file))
    original_lines = original_content.readlines()
    original_len = len(original_lines)
    original_size = os.path.getsize(os.path.join(original_dir,file))

    # Make Line
    if float(original_len)/float(original_size) <= 0.0008:
        original_content = open(os.path.join(original_dir,file))
        unformatted_content = BeautifulSoup(original_content,'lxml')
        formatted_content = unformatted_content.prettify()
        untagged_content = BeautifulSoup(formatted_content, 'html.parser').get_text().encode('utf8')
        original_content.close()

        # formatted_file = open(os.path.join(os.path.join(cleaned_dir, 'Manual_Clean'),file.split('.')[0] + '.txt'),'w')
        formatted_file = open(os.path.join(cleaned_dir,file.split('.')[0] + '.txt'),'w')
        untagged_content = untagged_content.split('\n')

        for uc in untagged_content:

            if '\xc3' or '\xbd' or '\xc2' or '\xa0' or '\xe2' or '\x80' or '\x99' or '\x9c' or '\x9d' or '\x94' or '\x97' or '\xa6' or '\xa2' or'\'' or '\x96' or '\xb7' or '\x92' or '\x93' or '\x8f' or '\x95' in uc:
                uc = uc.replace('\xc3','').replace('\xbd','').replace('\xc2','').replace('\xa0','').replace('\xe2','').replace('\x80','').replace('\x99','').replace('\x9c','').replace('\x9d','').replace('\x94','').replace('\x97','').replace('\xa6','').replace('\xa2','').replace("\'",r"'").replace('\x96','').replace('\xb7','').replace('\x92','').replace('\x93','').replace('\x8f','').replace('\x95','')

                if uc != '' and not uc.isspace():
                    formatted_file.write(uc.lstrip() + '\n')

        formatted_file.close()

    # Use the BeautifulSoup to clean the tags
    else:
        original_content = open(os.path.join(original_dir, file))
        untagged_content = BeautifulSoup(original_content,'html.parser').get_text().encode('utf8')
        original_content.close()

        untagged_file = open(os.path.join(cleaned_dir,file.split('.')[0] + '.txt'),'w')
        untagged_content = untagged_content.split('\n')

        for uc in untagged_content:

            if '\xc3' or '\xbd' or '\xc2' or '\xa0' or '\xe2' or '\x80' or '\x99' or '\x9c' or '\x9d' or '\x94' or '\x97' or '\xa6' or '\xa2' or'\'' or '\x96' or '\xb7' or '\x92' or '\x93' or '\x8f' or '\x95' in uc:
                uc = uc.replace('\xc3','').replace('\xbd','').replace('\xc2','').replace('\xa0','').replace('\xe2','').replace('\x80','').replace('\x99','').replace('\x9c','').replace('\x9d','').replace('\x94','').replace('\x97','').replace('\xa6','').replace('\xa2','').replace("\'",r"'").replace('\x96','').replace('\xb7','').replace('\x92','').replace('\x93','').replace('\x8f','').replace('\x95','')

                if uc != '' and not uc.isspace():
                    untagged_file.write(uc + '\n')

        untagged_file.close()



if __name__=='__main__':
    main()