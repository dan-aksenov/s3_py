# -*- coding: utf-8 -*-
from s3client import s3connect, buck_list

def main():
    s3connect( config_file = raw_input("Config file: ") )
    buck_list() 

if __name__ == '__main__':
    main()
