import codecs
import os

def get_stats(filename: str):
    print(filename + ' stats with byte alphabet:')
    # Num of bytes
    size = os.path.getsize(filename)
    print(f"size: {size}")

    # Counting inclusions of every byte
    inclusions = {}
    with open(filename, 'rb') as f:
        for i in range(0, size):
            # Reencoding every byte so python doesn't force ascii
            byte = codecs.encode(f.read(1), 'hex')
            try:
                inclusions[byte] += 1
            except KeyError:
                inclusions[byte] = 1

    print("\nInfo about bytes, sorted by inclusions")
    inclusions = sorted(inclusions.items(), key=lambda item: item[1], reverse=True)
    for k in inclusions:
        print(repr(f"Byte: {k[0]}, N of inclusions: {k[1]}"))


def sypher_columns(filename: str, col_num: int, kfilename: str):
    symbol = 'z'

    with open(kfilename, 'r') as kf:
        key = [int(x) for x in kf.readline().split()]
    print(key)

    size = os.path.getsize(filename)
    max_col_size = size / col_num
    file_bytes = []
    with open(filename, 'rb') as f:
        for sym in range(0, size):
            file_bytes.append(f.read(1))

    for i in range(col_num - size % col_num):
        file_bytes.append(bytes(symbol.encode()))

    new_size = len(file_bytes)
    with open("cyphered", "wb") as newfile:
        for col in range(col_num):
            index = key.index(col)
            for sym in range(0, new_size):
                if sym % col_num == index:
                    newfile.write(file_bytes[sym])


def desypher_columns(filename: str, col_num: int, kfilename: str):

    with open(kfilename, 'r') as kf:
        key = [int(x) for x in kf.readline().split()]

    size = os.path.getsize(filename)

    file_bytes = []
    with open(filename, 'rb') as f:
        for sym in range(0, size):
            file_bytes.append(f.read(1))

    row_num = int(size / col_num)
    with open("de_cyphered.doc", "wb") as newfile:
        for row in range(row_num):
            for item in key:
                newfile.write(file_bytes[row + row_num * item])

if __name__ == '__main__':
    file = '../../InformationProtection/TestText'
    get_stats(file)

    sypher_columns(file, 5, "key.txt")

    get_stats("cyphered")
    #get_stats_unicode(file)

    desypher_columns("cyphered", 5, "key.txt")