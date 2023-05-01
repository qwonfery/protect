NUM_OF_ROUNDS = 16
S_matrix = []
P_array = []


def to_32_bits(number: int) -> bytes:
    return number.to_bytes(4, 'big')


def to_int(number: bytes) -> int:
    return int.from_bytes(number, 'big')


def blowfish_encrypt_block(Ln: int, Rn: int, P: int) -> (int, int):
    new_R = Ln ^ P
    new_L = round_fun(to_32_bits(new_R)) ^ Rn
    return new_L, new_R


def feistel_network(Ln: int, Rn: int) -> (int, int):
    for i in range(NUM_OF_ROUNDS):
        Ln, Rn = blowfish_encrypt_block(Ln, Rn, P_array[i])
# меняем местами значения для 17 и 18 операции
    Ln, Rn = Rn, Ln

    Ln = Ln ^ P_array[NUM_OF_ROUNDS + 1]
    Rn = Rn ^ P_array[NUM_OF_ROUNDS]

    return Ln, Rn


# def de_feistel_network(Ln: int, Rn: int) -> (int, int):
#     Ln = Ln ^ P_array[NUM_OF_ROUNDS + 1]
#     Rn = Rn ^ P_array[NUM_OF_ROUNDS]
#
#     for i in range(NUM_OF_ROUNDS - 1, -1, -1):
#         Ln, Rn = blowfish_encrypt_block(Ln, Rn, P_array[i])
#
#     Ln, Rn = Rn, Ln
#
#     return Ln, Rn


def de_feistel_network(Ln: int, Rn: int) -> (int, int):

    for i in range(NUM_OF_ROUNDS + 1, 1, -1):
        Ln, Rn = blowfish_encrypt_block(Ln, Rn, P_array[i])

    Ln, Rn = Rn, Ln

    Ln = Ln ^ P_array[0]
    Rn = Rn ^ P_array[1]

    return Ln, Rn


# функция раунда(итерации)
def round_fun(number: bytes) -> int:
    # делим входящее число на 4 части по 8 бит
    ab = list(number)
    x1, x2, x3, x4 = (int.from_bytes(number[i:i + 1], 'big') for i in range(0, len(number), 1))

    result = (S_matrix[0][x1] + S_matrix[1][x2]) % (2**32)
    result = result ^ S_matrix[2][x3]
    result = (result + S_matrix[3][x4]) % (2**32)
    return result


# функция расширения ключа
# -> tuple(p_array,s_matrix)
def key_extension(key: bytes):
    P_CAPACITY = NUM_OF_ROUNDS + 2
    global S_matrix
    global P_array
    S_matrix = []
    P_array = []

    ## конкатенация ключа
    key = key * ((P_CAPACITY * 4) // len(key) + 1)
    key_len = len(key)
    key_array_32 = [to_int(key[i:i + 4]) for i in range(0, (P_CAPACITY * 4), 4)]


    # первичное заполенние S и P матриц через число Пи
    with open("../../InformationProtection/pi", "r") as f:
        ONE_NUMBER_LENGTH = 8

        for i in range(P_CAPACITY):
            P_pi = int(f.read(ONE_NUMBER_LENGTH).replace('\n', ''), 16)
            P_array.append(P_pi ^ key_array_32[i])

        for i in range(4):
            Sn_array = []
            for j in range(256):
                Sn_array.append(int(f.read(ONE_NUMBER_LENGTH).replace('\n', ''), 16))
            S_matrix.append(Sn_array)

    # вычисление новых значений раундовых ключей и матриц подстановки

    L0 = 0
    R0 = 0
    for i in range(0, P_CAPACITY, 2):
    # for i in range(17):
        L0, R0 = feistel_network(L0, R0)
        P_array[i], P_array[i + 1] = L0, R0

    for i in range(4):
        for j in range(0, 256, 2):
        # for j in range(255):
            L0, R0 = feistel_network(L0, R0)
            S_matrix[i][j], S_matrix[i][j + 1] = L0, R0

    a = 0


# сама шифрация
def cypher(filename: str, key: bytes) -> bytes:
    key_extension(key)
    cyphered = b''
    with open(filename, 'br') as f:
        text = f.read()

    # text = [text[i:i + 4] for i in range(0, len(text), 4)]
    text = [[text[i:i + 4], text[i + 4: i + 8]] for i in range(0, len(text), 8)]
    textoid = [(to_int(pare[0]),to_int(pare[1])) for pare in text]
    # print(textoid)
    # print(text)
    for pare in text:
        part1, part2 = feistel_network(to_int(pare[0]), to_int(pare[1]))
        cyphered += to_32_bits(part1) + to_32_bits(part2)

    with open("cyphered.txt", 'wb') as f:
        f.write(cyphered)

    return cyphered


# дешифрация
def decypher(filename: str, key: bytes) -> str:
    key_extension(key)

    with open(filename, 'br') as f:
        text = f.read()

    text_raw = [(to_int(text[i:i + 4]), to_int(text[i + 4:i + 8])) for i in range(0, len(text), 8)]
    text = bytearray()
    for i in range(len(text_raw)):
        text_raw[i] = de_feistel_network(text_raw[i][0], text_raw[i][1])
        text += delete_isignificant(text_raw[i][0]) + delete_isignificant(text_raw[i][1])
        # text += to_32_bits(text_raw[i][0]) + to_32_bits(text_raw[i][1])

    with open('de_cyphered', 'wb') as f:
        f.write(text)
    # print(text_raw)
    # print(text)
    text = text.decode(encoding='utf-8', errors='backslashreplace')

    return text


def delete_isignificant(bit32: int):
    return bit32.to_bytes(bit32.bit_length()//8 + (bit32.bit_length() % 8 != 0), 'big')


if __name__ == '__main__':
    filename = "../../InformationProtection/TestText"
    key = b'\x23\xff\x86\x64\x32\x86\x64\x32\x86\x64\x32\xff\xff\xaf\xfa'
    #key = b'0'
    cypher(filename, key)

    decyphered = decypher("cyphered.txt", key)
    print(decyphered)



