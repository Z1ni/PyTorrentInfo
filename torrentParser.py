# BitTorrent metafile handler (Bencoding/.torrent) for Python 3
# Mark "zini" Mäkinen 24.10.2014

# TODO: Create reading function to simplify readDict and readList
# TODO: Cleanup

LEVEL = -1  # Somewhat important only when debugging
DEBUG = False


def log(text):
    if DEBUG:
        print("  "*LEVEL + text)


def isNumeric(i):
    try:
        int(i)
        return True
    except ValueError:
        return False


def readDict(f, pos):
    global LEVEL
    LEVEL += 1
    log("readDict at %i" % pos)
    dictionary = {}
    key = None
    value = None
    f.seek(pos)
    c = True
    while c:
        c = f.read(1)
        try:
            d = c.decode("utf-8")
        except UnicodeDecodeError:
            pass

        if d == 'd':
            # Recursion!
            newD = readDict(f, f.tell())
            # Dictionaries can only be values?
            if value is None:
                value = newD

        if d == 'l':
            # List
            LEVEL += 1
            l = readList(f, f.tell())
            # Lists can only be values?
            if value is None:
                value = l
            LEVEL -= 1

        if isNumeric(d):
            # String
            LEVEL += 1
            f.seek(f.tell()-1)  # Start of the string, ex. 6:foobar
            s = readString(f, f.tell())
            if key is not None:
                # If key is set, this is the value
                value = s
            else:
                # If key isn't set, this is the key
                key = s
            LEVEL -= 1

        if d == 'i':
            # Integer
            LEVEL += 1
            f.seek(f.tell()-1)  # Start of the integer, ex. i42e
            i = readInt(f, f.tell())
            if key is not None:
                value = i
            else:
                key = i
            LEVEL -= 1

        if d == 'e':
            # Dict close
            LEVEL -= 1
            break

        if key is not None and value is not None:
            dictionary[key] = value
            key = None
            value = None

    return dictionary


def readList(f, pos):
    global LEVEL
    log("readList at %i" % pos)
    f.seek(pos)
    c = True

    list_values = []

    while c:
        c = f.read(1)
        try:
            d = c.decode("utf-8")
        except UnicodeDecodeError:
            pass

        if d == 'd':
            newD = readDict(f, f.tell())
            list_values.append(newD)

        if d == 'l':
            # List
            LEVEL += 1
            l = readList(f, f.tell())

            list_values.append(l)

            LEVEL -= 1

        if isNumeric(d):
            # String
            LEVEL += 1
            f.seek(f.tell()-1)  # Start of the string, ex. 6:foobar
            s = readString(f, f.tell())

            list_values.append(s)

            LEVEL -= 1

        if d == 'i':
            # Integer
            LEVEL += 1
            f.seek(f.tell()-1)  # Start of the integer, ex. i42e
            i = readInt(f, f.tell())

            list_values.append(i)

            LEVEL -= 1

        if d == 'e':
            # List end
            LEVEL -= 1
            break

    return list_values


def readInt(f, pos):
    global LEVEL
    log("readInt at %i" % pos)
    if f.read(1).decode("utf-8") == 'i':
        b = True
        num = ""
        while b:
            try:
                d = f.read(1).decode("utf-8")
            except UnicodeDecodeError:
                raise ValueError("Malformed integer: UnicodeDecodeError")
            if isNumeric(d):
                num += d
            else:
                if d == 'e':
                    # Correctly read integer
                    break
                else:
                    raise ValueError("Malformed integer")
        realInt = int(num)
        LEVEL += 1
        log("Int: %i" % realInt)
        LEVEL -= 1
        return realInt
    else:
        raise ValueError("Malformed integer")


def readString(f, pos):
    global LEVEL
    log("readString at %i" % pos)
    # Read the length of the string
    f.seek(pos)
    b = True
    len_text = ""
    while b:
        b = f.read(1)
        try:
            d = b.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("Malformed UTF-8 string")
        if isNumeric(d):
            len_text += d
        else:
            break
    str_len = int(len_text)     # Now we have the length of the string

    # Read the string
    string = f.read(str_len)
    try:
        utfString = string.decode("utf-8")
        LEVEL += 1
        log("String: %s" % utfString)
        LEVEL -= 1
        return utfString
    except UnicodeDecodeError:
        # Data
        LEVEL += 1
        log("Data")
        LEVEL -= 1
        return string


def readFile(path):

    f = open(path, "rb")

    # I think that there can't be multiple dictionaries at root level
    # Correct me if I'm wrong

    # dictList = []
    dictionary = {}

    c = f.read(1)
    while c:
        try:
            d = c.decode("utf-8")
        except UnicodeDecodeError:
            pass
        if d == 'd':
            # Dictionary
            # dictList.append(readDict(f, f.tell()))
            dictionary["torrent"] = readDict(f, f.tell())
        c = f.read(1)

    f.close()

    return dictionary


if __name__ == "__main__":

    readFile("test.torrent")
    exit()
