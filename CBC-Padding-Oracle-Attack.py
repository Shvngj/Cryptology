#!/usr/bin/env python
# coding: utf-8

# In[111]:


# 17. The CBC padding oracle
# https://www.youtube.com/watch?v=aH4DENMN_O4
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# PADDING ORACLE AVAILABLE TO ALL
def paddingoracle(plaintext):
    x = plaintext[-1]
    count = 0
    if x >= 1 or x <= 15:
        for i in range(-1,-16,-1):
            if plaintext[i] == x:
                count = count + 1
        if count == x:
            stripped_plaintext = plaintext.strip(chr(x).encode()*x)
            return True
        else:
            return False

# ENCRYPTION FROM ALICE'S SIDE
binary_data = b'AttackatdawnRunfarawayGoToTheMuseumofthedead'
l = len(binary_data)
m = (16 - l%16)%16
binary_data += chr(m).encode()*m

iv1 = get_random_bytes(16)
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv1)
ciphertext = cipher.encrypt(binary_data)

# ATTACK FROM OSCAR
if len(ciphertext)>16:
    iv2 = ciphertext[-32:-16]
    ciphertext = ciphertext[-16:]
else:
    iv2 = iv1

decipher = AES.new(key, AES.MODE_CBC, iv2)
plaintext = decipher.decrypt(totalciphertext)
reversed_cracked_plaintext = ''

modified_iv2 = bytearray(iv2)
for i in range(len(iv2)):
    #modified_iv2 = modified_iv2.replace(bytes(chr(modified_iv2[i]).encode()),bytes(chr(88).encode()))  
    modified_iv2[i] = 88       # replacing each character from front by 'X'
    decipher2 = AES.new(key, AES.MODE_CBC, modified_iv2)
    modified_plaintext = decipher2.decrypt(ciphertext)
    if paddingoracle(modified_plaintext)==False:
        index = 16-i              # padding given is index number
        break

for j in range(index,16):
    
    index = j
    modified_iv2 = bytearray(iv2)
    ciphertext = bytearray(ciphertext)
    
    for t in range(-1,-(index+1),-1):
        num = (modified_iv2[t]^plaintext[t])^(index+1)
        modified_iv2[t] = num
        
    #decipher4 = AES.new(key, AES.MODE_CBC, modified_iv2)
    #modified_plaintext = decipher4.decrypt(ciphertext)
    #print(modified_plaintext)  # b'ABCDEFGHIJKLM\x04\x04\x04'
    #print(modified_iv2)   # b'TANIYPRMONQSLC]P'
     
    for i in range(256):
        modified_iv2[-(index+1)] = i
        decipher3 = AES.new(key, AES.MODE_CBC, modified_iv2)
        modified_plaintext = decipher3.decrypt(ciphertext)
        #print(i,modified_iv2,modified_plaintext)
        if modified_plaintext[-(index+1)] == (index+1):
            number = i
            break

    # xoring to get plaintext bit
    xor = ((index+1))^(number^iv2[-(index+1)])
    reversed_cracked_plaintext += chr(xor)
    
cracked_plaintext = reversed_cracked_plaintext[::-1]
if len(cracked_plaintext) == 0:
    print('Padding was not required')
else:
    print(cracked_plaintext)

