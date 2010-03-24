import struct

# adopted from http://code.djangoproject.com/ticket/233
def imagesize(filename):
    try:
        fhandle = open(filename, 'rb')
    except:
        return
    head = fhandle.read(24)
    if len(head) != 24: return
    if head[:4] == '\x89PNG': # PNG
        check = struct.unpack('>i', head[4:8])[0]
        if check != 0x0d0a1a0a:
            return
        width, height = struct.unpack('>ii', head[16:24])
        img_type = 'PNG'
    elif head[:6] in ('GIF87a', 'GIF89a'): # GIF
        width, height = struct.unpack('<HH', head[6:10])
        img_type = 'GIF'
    elif head[:4] == '\xff\xd8\xff\xe0' and head[6:10] == 'JFIF': # JPEG
        img_type = 'JPEG'
        try:
            fhandle.seek(0)  # Read 0xff next
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf:
                fhandle.seek(size, 1)
                byte = fhandle.read(1)
                while ord(byte) == 0xff:
                    byte = fhandle.read(1)
                ftype = ord(byte)
                size = struct.unpack('>H', fhandle.read(2))[0] - 2
            # We are at a SOFn block
            fhandle.seek(1, 1)  # Skip `precision' byte.
            height, width = struct.unpack('>HH', fhandle.read(4))
        except Exception:
            return
    else:
        return
    return img_type, width, height

def adjustsize(sx, sy, w, h):
    try: outw = int(w)
    except:
        try: outw = float(w) * sx
        except:
            if str(w).endswith('%'): outw = int(w[:-1]) * 0.01 * sx
            else: outw = None
    try: outh = int(h)
    except:
        try: outh = float(h) * sy
        except:
            if str(h).endswith('%'): outh = int(h[:-1]) * 0.01 * sy
            else: outh = None

    if outw is None:
        if outh is None:
            outw = sx
            outh = sy
        else:
            outw = outh * sx / sy
    else:
        outh = outw * sy / sx
    return (int(round(outw)), int(round(outh)))

def imagesize_adjust(filename, w, h):
    size = imagesize(filename)
    if not size:
        try:
            return (int(w), int(h))
        except:
            return '', ''
    _, sx, sy = size
    return adjustsize(sx, sy, w, h)

