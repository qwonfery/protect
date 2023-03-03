
def byte_from_pixel():
    pass


def decoder(filename: str):
    with open(filename, "rb") as f:
        f.seek(10)
        off_to_raster = int.from_bytes(f.read(4), byteorder="little")

        f.seek(off_to_raster)
        text_bytes = bytearray()
        while pixel_byte := f.read(4):
            
            bytes += pixel_byte[-2:]
            #print(pixel_byte)
        print(bytes)


if __name__ == '__main__':
    file = "2.bmp"
    decoder(file)
