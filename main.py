# from typing import List
# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import HTMLResponse, FileResponse
# import mido
# import sys

# app = FastAPI()

# def bytes_to_int(byte):
#     result = 0
#     for b in byte:
#         result = result * 256 + int(b)
#     return result

# def special_pad(byte):
#     byte[0] = 128
#     byte[2] = 128
#     return byte

# def pad(byte, bit_1, bit_2):
#     if (bit_1 == 0 and bit_2 == 1):
#         # byte[0] = 128
#         # byte[1] = 128
#         byte[2] = 128
#     elif (bit_1 == 1 and bit_2 == 0):
#         byte[1] = 128
#         byte[2] = 128
#     elif (bit_1 == 1 and  bit_2 == 1):
#         byte[0] = 128
#         byte[2] = 128
#         byte[2] = 128
#     else:
#         return byte    
#     return byte

# def get_val(b):
#     print(b)

# def getbytes(bits, encoding):
#     done = False
#     while not done:
#         byte = 0
#         for i in range(0, 8):
#             try:
#                 bit = next(bits)
#             except StopIteration:
#                 bit = 0
#                 done = True
#             byte = (byte << 1) | bit
#             bits = bits.decode("utf-8")
#             encoding = bits
#             print(encoding)
#     yield byte

# def extract(byte):
#     if (byte[0] == 128 and byte[1] == 128 and byte[2] == 128):
#         value = "11"
#     elif (byte[1] == 128 and byte[2] == 128):
#         value = "10"
#     elif (byte[2] == 128):
#         value = "01"
#     else:
#         value = "00"
#     return value

# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     for file in files:
#         if file.content_type == 'audio/mid':
#             init_mid = mido.MidiFile(file=file.file)
#         elif file.content_type == 'text/plain':
#             with open(file.filename, 'rb') as secret:
#                 # Get the binary form of the secret file
#                 f = secret.read()
#                 b = bytes(f)
#     binary_secret = bin(int.from_bytes(b, byteorder=sys.byteorder))
#     x=len(binary_secret)
#     binary_secret = binary_secret[2:]
#     print("Binary form of secret message:", binary_secret)
    
#     # Iterating over the tracks
#     delta_times_playback = []
#     for msg in mido.merge_tracks(init_mid.tracks):
#         delta_times_playback.append(msg.time)
    
# new_bytes = []
# new_bytes_secret = []
    
# # print all the delta times with their respective 4 byte arrays
# for i in delta_times_playback:
#     byte = i.to_bytes(4, 'big')
#     byte = bytearray(byte)
#     new_bytes.append(byte)
    
# # Special padding to indicate start and stop
# new_bytes[0] = special_pad(new_bytes[0])
# new_bytes[len(binary_secret) + 2] = special_pad(new_bytes[len(binary_secret) + 2])
    
# print("\nSpecially padded start and stop bytes:")
# print(new_bytes[0])
# print(new_bytes[len(binary_secret) + 2])
    
# # Do the padding
# c=0
# for i in range(1, len(binary_secret), 2):
#     try:
#         new_bytes[i] = pad(new_bytes[i], binary_secret[c]), int(binary_secret[c + 1])
#     except:
#         new_bytes[i]=pad(new_bytes[c],binary_secret[i],0) 
#     new_bytes_secret.append(new_bytes[i])
#     print(new_bytes[i])
#     c+=2
                
# for i in range(0, len(new_bytes)):
# new_bytes[i] = bytes(new_bytes[i])
# new_bytes[i] = bytes_to_int(new_bytes[i])
    
# i = 0
# for msg in mido.merge_tracks(init_mid.tracks):
# msg.time = new_bytes[i]
# i += 1
    
# # Saving the modified song
# mid=mido.MidiFile()
# track=mido.MidiTrack()
# mid.tracks.append(track)
# for msg in mido.merge_tracks(init_mid.tracks):
#     track.append(msg)
# init_mid.save('stego.mid')
    
# # Extraction Algorithm
# # Open the MIDI File to read the hidden data
# secret_mid = mido.MidiFile('stego.mid')
    
# delta_times = []
# for msg in mido.merge_tracks(secret_mid.tracks):
#     delta_times.append(msg.time)
    
# secret_bytes = []
# for i in delta_times:
#     byte = i.to_bytes(4, 'big')
#     byte = bytearray(byte)
                    
# for i in secret_bytes:
#     secret_bytes.append(bytearray(i))
# final = []

# for i in secret_bytes:
#     final.append(extract(i))

#     # Finally print the extracted data
#     print("\nData from binary file as text:")
#     b = get_val(b)
#     getbytes(final_str, b)
    
#     return FileResponse("stego.mid")

# @app.get("/")
# def main():
#     return HTMLResponse(
#         content=open('index.html', 'r').read(),
#         status_code=200
#     )

# @app.get("/upload")
# def main():
#     return HTMLResponse(
#         content=open('upload.html', 'r').read(),
#         status_code=200
#     )








#new code 
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
import mido
import sys

app = FastAPI()

def bytes_to_int(byte):
    result = 0
    for b in byte:
        result = result * 256 + int(b)
    return result

def special_pad(byte):
    byte[0] = 128
    byte[2] = 128
    return byte

def pad(byte, bit_1, bit_2):
    if bit_1 == 0 and bit_2 == 1:
        byte[2] = 128
    elif bit_1 == 1 and bit_2 == 0:
        byte[1] = 128
        byte[2] = 128
    elif bit_1 == 1 and bit_2 == 1:
        byte[0] = 128
        byte[1] = 128
        byte[2] = 128
    else:
        return byte
    return byte

def get_val(b):
    print(b)

def getbytes(bits, encoding):
    done = False
    while not done:
        byte = 0
        for i in range(0, 8):
            try:
                bit = next(bits)
            except StopIteration:
                bit = 0
                done = True
            byte = (byte << 1) | bit
        bits = bits.decode("utf-8")
        encoding = bits
        print(encoding)
        yield byte

def extract(byte):
    if byte[0] == 128 and byte[1] == 128 and byte[2] == 128:
        value = "11"
    elif byte[1] == 128 and byte[2] == 128:
        value = "10"
    elif byte[2] == 128:
        value = "01"
    else:
        value = "00"
    return value

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        if file.content_type == 'audio/mid':
            init_mid = mido.MidiFile(file=file.file)
        elif file.content_type == 'text/plain':
            with open(file.filename, 'rb') as secret:
                # Get the binary form of the secret file
                f = secret.read()
                b = bytes(f)
                binary_secret = bin(int.from_bytes(b, byteorder=sys.byteorder))
                x = len(binary_secret)
                binary_secret = binary_secret[2:]
                print("Binary form of secret message:", binary_secret)

                # Iterating over the tracks
                delta_times_playback = []
                for msg in mido.merge_tracks(init_mid.tracks):
                    delta_times_playback.append(msg.time)

                new_bytes = []
                new_bytes_secret = []

                # Print all the delta times with their respective 4-byte arrays
                for i in delta_times_playback:
                    byte = i.to_bytes(4, 'big')
                    byte = bytearray(byte)
                    new_bytes.append(byte)

                # Special padding to indicate start and stop
                new_bytes[0] = special_pad(new_bytes[0])
                new_bytes[len(binary_secret) + 2] = special_pad(new_bytes[len(binary_secret) + 2])

                print("\nSpecially padded start and stop bytes:")
                print(new_bytes[0])
                print(new_bytes[len(binary_secret) + 2])

                # Do the padding
                c = 0
                for i in range(1, len(binary_secret), 2):
                    try:
                        new_bytes[i] = pad(new_bytes[i], int(binary_secret[c]), int(binary_secret[c + 1]))
                    except:
                        new_bytes[i] = pad(new_bytes[i], int(binary_secret[i]), 0)
                    new_bytes_secret.append(new_bytes[i])
                    print(new_bytes[i])
                    c += 2

                for i in range(0, len(new_bytes)):
                    new_bytes[i] = bytes(new_bytes[i])
                    new_bytes[i] = bytes_to_int(new_bytes[i])

                i = 0
                for msg in mido.merge_tracks(init_mid.tracks):
                    msg.time = new_bytes[i]
                    i += 1

                # Saving the modified song
                init_mid.save('stego.mid')

                # Extraction Algorithm
                # Open the MIDI File to read the hidden data
                secret_mid = mido.MidiFile('stego.mid')

                delta_times = []
                for msg in mido.merge_tracks(secret_mid.tracks):
                    delta_times.append(msg.time)

                secret_bytes = []
                for i in delta_times:
                    byte = i.to_bytes(4, 'big')
                    byte = bytearray(byte)
                    secret_bytes.append(bytearray(byte))

                final = []
                for i in secret_bytes:
                    final.append(extract(i))

                # Finally print the extracted data
                print("\nData from binary file as text:")
                for f in final:
                    print(get_val(f))

    return FileResponse("stego.mid")

@app.get("/index")
def main():
    return HTMLResponse(
        content=open('index.html', 'r').read(),
        status_code=200
    )

@app.get("/upload")
def main():
    return HTMLResponse(
        content=open('upload.html', 'r').read(),
        status_code=200
    )

