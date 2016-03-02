# -*-coding:utf-8 -*-
# 
# Created on 2016-03-01, by felix
# 

__author__ = 'felix'

import os


def main():
    f = open('company_list', 'r')
    for obj in f:
        print obj
        command = 'scrapy crawl user_info -a company_name=%s' % obj
        os.popen(command)

if __name__ == '__main__':
    main()
