#!//bin/python
from s3client import s3connect, buck_dump_diff
import sys
from getopt import getopt

def usage():
    '''Функция "Инструкция по пременению" '''
    
    print "Usage: -c config file path, -b bucket name, -d backup directory"


def main():
    try:    
        opts, args = getopt( sys.argv[1:], 'c:b:d:' )
    except:
        usage()
        sys.exit(1)

    # Назначение переменныч c - config file, b - bucket name, d - dump directory
    for opt, arg in opts:
        if opt in ( '-c' ):
            config_file = arg
        elif opt in ( '-b' ):
            buck_name = arg
        elif opt in ( '-d' ):
            dump_path = arg
        else:
            usage()
            sys.exit(1)

    try:
        config_file
    except:
        config_file = raw_input('Config file path: ')
    
    try:
        buck_name
    except:
        buck_name = raw_input('Bucket to dump:  ')
    
    try:
        dump_path
    except:
        dump_path = raw_input('Dump directory: ')
            
    s3connect( config_file )
    buck_dump_diff( buck_name, dump_path )


if __name__ == '__main__':
    main()