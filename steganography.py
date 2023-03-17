
def decoder(filename: str):
    with open(filename, "rb") as f:
        f.seek(10)
        off_to_raster = int.from_bytes(f.read(4), byteorder="little")

        f.seek(off_to_raster)
        text_bytes = bytearray()

        while pixel := f.read(4):

            FF = int.from_bytes(b'\xFF', 'big')
            pixel = int.from_bytes(pixel, 'big')

            blue = (pixel >> 3 * 8) & FF
            blue_bits = get_last2_bits(blue) << 6

            green = (pixel >> 2 * 8) & FF
            green_bits = get_last2_bits(green) << 4

            red = (pixel >> 1 * 8) & FF
            red_bits = get_last2_bits(red) << 2

            reserved = pixel & FF
            reserved_bits = get_last2_bits(reserved)

            cyphered_byte = blue_bits | green_bits | red_bits | reserved_bits

            text_bytes.append(cyphered_byte)
            if cyphered_byte == int.from_bytes(b'\xFF', 'big'):
                break

        print(text_bytes.decode(errors='backslashreplace'))


def coder(picfilename, textfilename):

    with open(textfilename, 'rb') as f:
        text_bytes = f.read()

    # with open(picfilename, "rb") as f:
    #     file_bytes = f.read()

    with open(picfilename, "rb+") as f:
        f.seek(10)
        off_to_raster = int.from_bytes(f.read(4), byteorder="little")

        f.seek(off_to_raster)
        FC = int.from_bytes(b'\xFC', 'big')
        FF = int.from_bytes(b'\xFF', 'big')

        for byte in text_bytes:
            blue_m, green_m, red_m, reserved_m = substract_byte(byte)
            pixel = f.read(4)
            f.seek(-4, 1)
            pixel = int.from_bytes(pixel, 'big')

            blue = (pixel >> 3 * 8) & FC
            blue = blue | blue_m
            f.write(blue.to_bytes(8, 'big'))

            green = (pixel >> 2 * 8) & FC
            green = green | green_m
            f.write(green.to_bytes(8, 'big'))

            red = (pixel >> 1 * 8) & FC
            red = red | red_m
            f.write(red.to_bytes(8, 'big'))

            reserved = pixel & FC
            reserved = reserved | reserved_m
            f.write(reserved.to_bytes(8, 'big'))



            #text_bytes.append(cyphered_byte)

        #print(text_bytes.decode(errors='backslashreplace'))

    pass


def get_last2_bits(byte: int):
    last2_bits_number = int.from_bytes(b'\x03', 'big')
    return byte & last2_bits_number


def substract_byte(byte: int):
    blue = get_last2_bits(byte >> 6)
    green = get_last2_bits(byte >> 4)
    red = get_last2_bits(byte >> 2)
    reserved = get_last2_bits(byte)
    return blue, green, red, reserved


if __name__ == '__main__':
    file = "2copy.bmp"
    #file = "Лабораторная работа 3_варианты/7.bmp"
    #decoder(file)
    coder(file, "TestText")
