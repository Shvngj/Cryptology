#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# For reference check the below sites:
# https://thmsdnnr.com/tutorials/javascript/cryptopals/2017/09/16/cryptopals-set1-challenge-6-break-repeating-key-XOR.html
# https://laconicwolf.com/2018/06/30/cryptopals-challenge-6-break-repeating-key-xor/

from binascii import hexlify, unhexlify
from base64 import b64decode, b64encode

def encryption(pt,k):
    #pt = b"Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
    #k = b"LOTUS"
    ct = b''
    for i in range(len(pt)):    
        m = pt[i] ^ k[i%len(k)]
        r = chr(m).encode()
        ct += r
    return ct

def partofHD(m,n):  
    c = 0
    x = m^n
    q = x
    while(q>0):
        q = (int)(x/2)
        r = x%2
        x = q
        if(r != 0):
            c=c+1
    return c

def HD(a,b):
    HD = 0
    for i in range(len(a)):
        HD += partofHD(a[i],b[i])
    return HD

File_obj = open(r"S1C6.txt","r")
inp = File_obj.read()
inp = b64decode(inp)
#ascii_inp = []
#ascii_inp += [inp[i] for i in range(len(inp))]  # len(ascii_inp) = 2876


# In[ ]:


keysize = []
av_dist = []

for ks in range(2,41):
    chunksofks = [inp[i:i+ks] for i in range(0,len(inp),ks)]
    distances = []
    sum_of_dist = 0
    while True:
        try:
            dist = HD(chunksofks[0],chunksofks[1]) / ks
            sum_of_dist += dist
            distances.append(dist)
            del chunksofks[0]
            del chunksofks[0]
        except:
            break
    av_of_all_dist_in_distances_of_ks = sum_of_dist/len(distances)
    keysize.append(ks)
    av_dist.append(av_of_all_dist_in_distances_of_ks)

ks_avdist = {keysize[i]:av_dist[i] for i in range(len(keysize))}

KsandScore = sorted(ks_avdist.items(), key = lambda x: x[1])[0]  # (29, 2.771287825475019)
KEYSIZE = KsandScore[0]   # 29
SCORE = KsandScore[1]   # 2.771287825475019
print(KsandScore)


# In[ ]:


"""
THIS IS HOW THE EXCEPTION WORKS

x = b'ABCDEFGHI'
for ks in range(2,3):
    chunksofk = [x[i:i+ks] for i in range(0,len(x),ks)]
    print(chunksofk)
    distances = []
    while True:
        try:
            dist = HD(chunksofk[0],chunksofk[1])
            print(dist)
            distances.append(dist/ks)
            print(distances)
            del chunksofk[0]
            print(chunksofk)
            del chunksofk[0]
            print(chunksofk)
        except Exception as e:
            break
"""


# In[ ]:


numof_bytes_to_be_removed = len(inp)%KEYSIZE
originalinp = inp
inp = inp[:len(inp)-numof_bytes_to_be_removed]
chunksofct = []
for j in range(KEYSIZE):
    string = b''
    for i in range(j,len(inp),KEYSIZE):
        string += chr(inp[i]).encode()
    chunksofct.append(string)
print(chunksofct)


# In[ ]:


# Using character freq to solve for key
ch_freq = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }

keyvalue = b''
for i in range(len(chunksofct)):
    scoreforkey = {}
    for k in range(256):
        cipherstring = chunksofct[i]
        plainstring = encryption(cipherstring,chr(k).encode())
        scoreofakeyforachunk = 0
        scoreofakeyforachunk = sum([ch_freq.get(chr(byte), 0) for byte in plainstring.lower()])
        
        #for j in range(len(plainstring)):
            #ch = plainstring[j]
            #if (65<=ch and ch<= 90) or (97<=ch and ch<=122):
                #scoreofakeyforachunk = scoreofakeyforachunk + ch_freq[chr(ch)]
        
        scoreforkey[k] = scoreofakeyforachunk
    sortedscoreforkey = sorted(scoreforkey.items(), key = lambda x:x[1],reverse=True)[0]
    keyvalue += chr(sortedscoreforkey[0]).encode()
#print(keyvalue)  # b'Terminator X: Bring the noise'
DECRYPTED_PLAINTEXT = encryption(originalinp,keyvalue)
#print(DECRYPTED_PLAINTEXT)


# In[ ]:


# counting the number of alphabets in decrypted text to find key : Less accuracy than the previous.
keyvalue1 = b''
for i in range(len(chunksofct)):
    numalphaforkey = {}
    for k in range(256):
        cipherstring1 = chunksofct[i]
        plainstring1 = encryption(cipherstring1,chr(k).encode())
        plainstring1 = plainstring1.lower()
        
        numofalphaofakeyforachunk = 0
        for j in range(len(plainstring1)):
            ch = plainstring1[j]
            if (97<=ch and ch<=122):
                numofalphaofakeyforachunk = numofalphaofakeyforachunk + 1
        
        numalphaforkey[k] = numofalphaofakeyforachunk
    sortedscoreforkey1 = sorted(numalphaforkey.items(), key = lambda x:x[1],reverse=True)[0]
    keyvalue1 += chr(sortedscoreforkey1[0]).encode()
#print(keyvalue1) # b'Terminator X: Bring the noise'
DECRYPTED_PLAINTEXT1 = encryption(originalinp,keyvalue1)
#print(DECRYPTED_PLAINTEXT1)

