# Baby RSA 

* ## Understanding the Code
This challenge is typically a RSA Challenge but with a little twist.
For those who aren't still familiar with this type of algorithm, [Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
has explained it in detail.
The source code is given in the challenge:
```python
from Crypto.Util.number import getPrime, getRandomRange
FLAG = 'FindITCTF{REDACTED}'

p = getPrime(1024)
q = getPrime(1024)
N = p*q
e = 0x10001 #65537
N_masked = list(str(N))
for _ in range(6):
N_masked[getRandomRange(0, len(N_masked))] = 'x' #This part will replace certain number randomly from N with 'x'
N_masked = "".join(N_masked)
print(f"N_masked = {N_masked}")
C = [pow(ord(c), e, N)>>1 for c in FLAG] #RSA Algorithm
print(f"C = {C}")
```
You may download the source of the challenges from here.
At first, it's a prerequisite for RSA to have the distinct prime numbers which
are selected and assigned to the variables `p` and `q` which have their own
size of 1024 bits (yet these could be varied).

The `N` variable will contain the modulus which will later be used for encrypting and
decrypting the message. We also have the `e` with a value of 65537.
The `C` variable is a list which holds the ciphertext of the RSA.

* ## Breaking RSA
Breaking RSA should be trivial especially for the basics one, we could redo and re-implement
the algorithm above, yet we need to **brute-force** some of the numbers that were replaced by 
the 'x'.

Here's the script that would find the respective x's:
```python
import string
from Crypto.Util.number import *
numbers = "0123456789"
e = 0x10001

cipher =
[24301980541718133564685704192002712194490765766789773307021553846164
229665364399841496527879043477862519917347609920634635501390878515267
842242598236078864645688112788610606926296244175778361808539270376332
928062154477794906730095965969335651737075001150863849529259647081160
156442623747672276278070099029365138641776022278089223813428036705917
070304223502871149606833719885150087877691166239028202707081425246506
082870157913644918283423118729882296712750522382804481629234958684286
689276340755446935712343789582288199905375667153496202580066249252990
64003360157815357972581580801369171231235122802277830482900918219,
956672832150073487662553160334853411179900264321023152052565727649308
574366832962328919364515181377603447766790799891800847557138628789276
256710129091126018400778155139732351312983113150353009762645863952268
797609702529864367312124384280578850701568689499477266066752766258888
131489799363497695711724891669728373384911552717643337116497531515754
654853383561716207415364327167709913155485732059030855508177094056362
674921568510660710188337267970974115852619521473037617023809582538150
426376696151007422293213226333771972865252981603256355714959915323383
3837581337661540637765323387545072325898460279541349918485654224,
....] #etc :)

for i in numbers:
  for j in numbers:
    for k in numbers:
      for l in numbers:
        for m in numbers:
          for n in numbers:
            print(i, j, k, l, m, n)
            N_baru = str(21022850466621037769708677576925994323799557100753480004047244311247904448349530332497012095272352769059840683329533206682874110) + i + str(289126845969366352627121095133697653792615564277853968085374458187497270011357018991524922740682560909276968423432230525022773410732626759045003404453844514854089059052168106105408307) + j + str(70802712764976697277408322943223343255363381115432845840845941253305324016139244019454699910693785375999481543635730084790753124753680354721534315616158297852604043938719783) + k + str(73397) + l +str(46442242145088603060181358033531883703753) + m + str(3374330449276881764159676919120402711238866891557) + n + str(60413515481545371406947204366503)
            if (pow(70,e,int(N_baru)) >> 1) == cipher[0]: #Since we know the flag starts with 'F' and ord('F') == 70 :) We could use it for a faster search
               print("FOUND IT!")
               break
```

It takes less than 2 minutes to find the respective x's:
```bash
python test.py > test.txt
cat test.txt| grep FOUND -B 4
('1', '3', '3', '8', '5', '8')
('1', '3', '3', '8', '5', '9')
('1', '3', '3', '8', '6', '0')
('1', '3', '3', '8', '6', '1')
FOUND IT!
```

So we can conclude that the respective x's should be:
```python
x[0] = x[5] = 1
x[1] = x[2] = 3
x[3] = 8
x[4] = 6
```

Append these scripts to the prior solver and we got the flag:
```python
flag=""

for w in cipher:
  for x in range(256):
    res = pow(x, e, int(N_baru)) >> 1
    if res == w:
      flag+=chr(x)

print(flag)
#FindITCTF{R1v3575H4M1r4dl3M4n_bF}
```

The challenge's description said that there are some unprintable ASCII code.
Turns out it's the `–` between the 3 people's name that found RSA!

`Flag: FindITCTF{R1v357–5H4M1r–4dl3M4n_bF}`
