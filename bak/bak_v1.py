import sys

def main():
    print('bat - a simple backup tool')
    if len(sys.argv) == 1:
        print('Usage: bat [file]')
        sys.exit(1)
    filename = sys.argv[1]
    backup_filename = filename + '.bak'
    with open(backup_filename, 'w') as file_write:
        with open(filename, 'r') as file_read:
            file_write.write(file_read.read())
    return

if __name__ == "__main__":
    main()
