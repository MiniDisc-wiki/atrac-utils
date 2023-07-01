def aea_header(channels = 2):
    # This isn't a very complete implementation
    header = bytearray()
    header += (2048).to_bytes(4, 'little')
    header += (0).to_bytes(256, 'little')
    header += (1).to_bytes(4, 'little')
    header += channels.to_bytes(1, 'little')
    header += (0).to_bytes(2048-len(header), 'little')
    return header

def generate_header(format, length):
    header = bytearray()
    match format:
        case "LP2":
            bytesPerFrame = 192
            jointStereo = 0
        case "LP4":
            bytesPerFrame = 96
            jointStereo = 1
    bytesPerSecond = (bytesPerFrame * 44100) // 512

    header += bytes('RIFF', 'ascii')
    header += (length + 60).to_bytes(4,'little')
    header += bytes('WAVEfmt ', 'ascii')
    header += (32).to_bytes(4,'little')
    header += (0x270).to_bytes(2,'little') # ATRAC3
    header += (2).to_bytes(2, 'little') # two channels
    header += (44100).to_bytes(4,'little') # sample rate
    header += bytesPerSecond.to_bytes(4, 'little')
    header += (bytesPerFrame * 2).to_bytes(2, 'little')
    header += (0).to_bytes(2, 'little') 
    header += (14).to_bytes(2, 'little')
    header += (1).to_bytes(2, 'little')
    header += bytesPerFrame.to_bytes(4, 'little')
    header += jointStereo.to_bytes(2, 'little')
    header += jointStereo.to_bytes(2, 'little')
    header += (1).to_bytes(2, 'little')
    header += (0).to_bytes(2, 'little')
    header += bytes('data', 'ascii')
    header += length.to_bytes(4, 'little')
    return header

def validate_header(file):
    attributes = {}
    if file.read(4) != bytes('RIFF', 'ascii'):
            raise IOError("Not a WAV encapsulated file")
    file.read(4) # Throw away the file length
    if file.read(8) != bytes('WAVEfmt ', 'ascii'):
            raise IOError("Broken WAV file")
    file.read(4) # Throw away the next 4 bytes
    if file.read(2) != (0x270).to_bytes(2,'little'):
            raise IOError("WAV file doesn't contain ATRAC3")
    file.read(6) # Throw away channel count/sample rate
    bytesPerFrame = round(int.from_bytes(file.read(4), 'little') * 512 / 44100)
    print(f'bytesPerFrame : {bytesPerFrame}')
    if bytesPerFrame == 96:
         attributes["mode"] = 'LP4'
    elif bytesPerFrame == 192:
         attributes["mode"] = 'LP2'
    else:
        raise IOError("Unknown ATRAC3 encoding")
    file.read(20) # get to the end of the header
    if file.read(4) != bytes('data', 'ascii'):
            raise IOError("Not a WAV encapsulated file")
    file.read(4)
    return attributes
