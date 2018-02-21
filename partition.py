#!/usr/bin/env python3

import wave
from struct import pack, unpack, calcsize
from tqdm import tqdm


filepath = "42-01.wav"

f = wave.open(filepath,"rb")  

rate = f.getframerate()
totalFrames = f.getnframes()
channels = f.getnchannels()
sampWidth = f.getsampwidth()
length = float(totalFrames)/rate # total length in seconds

chunkLength = 30.0 # in seconds
totalChunks = length/chunkLength 
remainder = totalFrames%(chunkLength*rate) # last chunk

# print(chunkLength, totalChunks, remainder)

print("\n\nopening: "+filepath)
print("samplerate: "+str(f.getframerate()))
print("frames: "+str(f.getnframes()))
print("channels: "+str(f.getnchannels()))
print("sample width: "+str(f.getsampwidth()))

# -- get all samples ----------------------------------------
s = f.readframes(totalFrames)
unpstr = '<{0}h'.format(totalFrames*channels)
bytesamples = list(unpack(unpstr, s)) # convert the byte string into a list of ints
samples = []
for e in bytesamples:
    samples.append(bytesamples[e])



# -- segment samples ----------------------------------------
def segmentize(samps):
    for i in tqdm(range(0,totalChunks)):
        # ...



# -- open wave file -----------------------------------------
wv0 = wave.open("chunks/test.wav", 'w')
wv0.setparams((channels, sampWidth, rate, 0, 'NONE', 'not compressed'))

def write_data():
    writeData = b""
    print("writing data...")
    for i in range(0,(totalFrames*2)):
        samp = int(samples[i])
        writeData += pack('h', samp)
    wv0.writeframes(writeData)
    wv0.close()

write_data()