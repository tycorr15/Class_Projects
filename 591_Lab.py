#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################## LAB 10 ##############################################

"""
List you collaborators here:
                                party one 
                                party two...


Your task is to fill in the body of the functions below. The specification of each of the functions is commented out.
"""
import lab10_helper
from Cryptodome.Hash import HMAC
from Cryptodome.Hash import SHA as SHA1
from Cryptodome.Hash import SHA256
from hashlib import md5



def hmacsha1(key, message):
    return HMAC.new(key, message, SHA1).hexdigest()

def hmacsha2(key, message):
    return HMAC.new(key, message, SHA256).hexdigest()



def q1_fb_onion_hash(password, salt1, salt2):
    """Question 1: Implement Facebook's Onion Hash
    
    To solve this problem, they could simply wait until the next user login and
    then compute both hashes of the password: one to validate the user login and
    the other to store an upgraded version for next time.

    That solution would work great for users who log in frequently. But there
    are plenty of people who haven't logged into Facebook in years, and it'd be
    great to provide them with stronger security too when newer hash functions
    are built.
    
    Therefore, a better solution is to nest one hash function on top of the
    other:  `SHA1(MD5(password))`. This 'nested' solution enables Facebook to
    upgrade their password hashes without user input.

    Facebook has followed this `onion' approach as they migrated to stronger and
    stronger hash functions, including ones like `scrypt` that are built
    specifically for protecting passwords.

    The pseudocode for "The Onion" approach can be summarized as follows:
    ```
        cur     = 'plaintext'
        cur     = md5(cur)
        salt    = randbytes(20)
        cur     = hmac_sha1(cur, salt)
        cur     = cryptosystem::hmac(cur)
               [= hmac_sha256(cur, secret)]
        cur     = scrypt(cur, salt)
        cur     = hmac_sha256(cur, salt)
    ```
    (pseudocode was retrieved from this talk by Alex Muffet (from Facebook) at
    Passwords14, link:https://youtu.be/7dPRFoKteIU?t=132 relevent slide at 2:12)

    Your Task:
        Implement the first 5 lines of the Facebook onion hash. Ignore the final
        2 lines. That is, write a function that does the following
        transformation to any password: apply MD-5, take that result and apply
        HMAC-SHA1 with a provided salt, and finally take that result and apply
        HMAC-SHA256 with another provided salt. Make sure that you pass along
        the results from one to the other as binary bitstrings. The final result
        must be hex-encoded though so that it is safe to store in a database.

        Use the salt as the secret key portion of the HMAC. You may find the 
        solutions from the previous labs useful when constructing the HMAC.
        
    
    Args:
        password    (str):  ASCII-encoded user input password
        salt1       (str):  ASCII-encoded salt to be used with the HMAC-SHA1
        salt2       (str):  ASCII-encoded salt to be used with the HMAC-SHA256
    
    Output:
        ret         (str):  Hex-encoded hash output after applying the protocol
                            described above. 
    
    How to verify your solution:
    ```
        assert(q1_fb_onion_hash('Password1!', 'salt1', 'salt2') 
            == '06912315b30054d76340a880dbb7b65d366df1f8dee1c348aa1bc4354f42cc38')
    ```
    """
    
    new_pass = password.encode('ASCII')
    ans = (md5(new_pass).hexdigest())
    this = bytes.fromhex(ans)
    
    salt1 = salt1.encode('ASCII')
    salt2 = salt2.encode('ASCII')
    
    that = hmacsha1(salt1, this)
    
    that = bytes.fromhex(that)
    answer = hmacsha2(salt2, that)
    
    return answer

    



def parse_and_hash(string):
    lines = string.split("\n")
        
        
    arr = [0] * len(lines[0])
    i = 0
    
    for c in lines[0]:
        if (c == '$'or c == ':'):
            arr[i] = 'space'
            i += 1
        else:
            arr[i] = c
            i += 1

    k = 0
    index = [0] * 20
    for j in range(len(arr)):
        if (arr[j] == 'space'):
            index[k] = j
            k += 1
    
    number = arr[(index[1] + 1):index[2]]
    salt = arr[(index[2] + 1): index[3]]
    hashy = arr[(index[3]+ 1): index[4]]
    salt = ''.join(salt)
    hashy = ''.join(hashy)
    number = int(number[0])
    
    passwords = lab10_helper.top_rockyou_passwords
    
    for i in range(len(passwords)):
        hash_pass = lab10_helper.hash_password(number, salt, passwords[i])
        if (hashy in hash_pass):
           ans1 = passwords[i]
        else:
            i += 1
    return ans1

def q2_crack_shadow(shadow_file):
    """Question 2: Crack /etc/shadow file

    The `/etc/shadow` file (on GNU/Linux) stores the hashes of the actual
    passwords for all the user’s accounts (If you're using a Linux OS, you can
    check the file yourself). The `shadow` file also stores additional
    properties related to user password, so basically, it stores secure
    user account information. 
    Within the `shadow` file, each entry (line) represents a password for a
    specific user, so if your system contains three users, you should expect the
    `shadow` file to contain three entries at least.

    According to the `shadow` file specification, here is an example of an entry
    in the `shadow` file:    
    ```
    root:$1$TDQFedzX$.kv51AjM.FInu0lrH1dY30:15045:0:99999:7:::
      ^   ^     ^               ^             ^   ^   ^   ^
      |   |     |               |             |   |   |   |
      1   2     3               4             5   6   7   8
    ```

    All fields (within an entry) are separated by a colon (:) symbol. Password
    related parameters are further separated by a dollar sign ($) symbol.

    For the purposes of this lab, we would only focus on 2, 3 and 4 (from the
    example above):
    2: `id`: the hash algorithm used, on GNU/Linux the mapping is as follows:
                $1$ is MD5
                $2a$ is Blowfish
                $2y$ is Blowfish
                $5$ is SHA-256
                $6$ is SHA-512
    3:  `salt`: salt value is nothing but a random value (ascii-encoded) that's 
                generated to combine with the original password, the same concept 
                is discussed in lecture 18 slides.
    4:  `password_hash`: the hash value (variant of base64 encoded) of salt +
                        user password given the `id` hash algorithm and the salt 
                        provided.

    Args:
        shadow_file         (str):  ASCII-encoded contents of a shadow file,
                                    this value is exactly equivalent to 
                                     `open('/etc/shadow', 'r').read()`
                                (Note: file lines are seperated by `\n`, check 
                                       `lab10_helper.sample_shadow_file` for an 
                                        example)
    Output:
        ret         (list(str)):    List of the ASCII-encoded cracked
                                    passwords extracted from the given shadow
                                    file. The passwords are expected to be in 
                                    the same order as they were in the shadow 
                                    file.
    
    How to verify your solution:
    ```
        assert(lab10_helper.hash_answer(q2_crack_shadow(lab10_helper.sample_shadow_file)) 
            == "136b67895d86122c443c93d23f1c6102e2fcff588be789983bd116ce109ff286")
    ```
    """
    
    lines = shadow_file.split('\n')
    ans_arr = [0]* (len(lines) - 1)
    for i in range(len(lines) - 1):
        ans_arr[i] = parse_and_hash(lines[i])
         
        
    return ans_arr
