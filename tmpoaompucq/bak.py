import sys


def main():
    print("bat - a simple backup tool")

    # show help if no args
    if len(sys.argv) == 1:
        print("Usage: bat [file]")
        sys.exit(1)
    filename = sys.argv[1]

    # figure out the backup filename
    backup_filename = filename + ".bak"

    # write the content byte-for-byte
    with open(backup_filename, "w") as file_write:
        with open(filename, "r") as file_read:
            file_write.write(file_read.read())
    return


if __name__ == "__main__":
    main()
