from s3client import s3connect, buck_dump_diff

def main():
    s3connect( config_file = raw_input("Config file: ") )
    buck_dump_diff( buck_name = raw_input("Bucket: "), dump_path = raw_input("Dump path: ") )

if __name__ == '__main__':
    main()
