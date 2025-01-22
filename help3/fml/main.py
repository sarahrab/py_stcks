from console_io import ConsoleReader, ConsoleWriter

reader = ConsoleReader()
writer = ConsoleWriter()


if __name__ == '__main__':
    writer.write("Hello")
    count = reader.read_int("Enter number of strings: ")
    for i in range(0, count):
        s = reader.read_string("Enter your text: ")
        writer.write(f"{i}: {s}")