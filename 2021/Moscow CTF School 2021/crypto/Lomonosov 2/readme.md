# Lomonosov 2
_У нас в МГУ есть суперкомпьютер, и мы с его помощью кое-что зашифровали._

[encrypt.py](encrypt.py)

[output.txt](output.txt)

### Решение
Рассмотрим файл `encrypt.py`

В нём генерируются 2 простых числа `p` и `n`. Затем с помощью функции `v` получают ключ и ксорят его с флагом.
Числа `p` и `n` и зашифрованный флаг нам дан, поэтому, чтобы восстановить флаг, нужно восстановить ключ (т.к. `(a ^ b) ^ b = a`).

Запускать функцию `v` с заданными параметрами нецелесообразно, так как считается факториал числа `n` (а оно 2048ми-битное). Поэтому разберём, что делает данная функция. Она считает, сколько раз `n!` делится нацело на `p`. Чтобы посчитать, представим `n!` в виде произведения:

`n! = 1 * 2 * 3 * 4 * ... * p * (p + 1) * (p + 2) * ... * (p + p) * ... * (p + p + p) * ... * n`

`n! = 1 * 2 * 3 * 4 * ... * p * (p + 1) * (p + 2) * ... * (2 * p) * ... * (3 * p) * ... * (k * p) * ... * n`

Заметим, что `p` встречается в произведении ровно `k` раз (`k` - целое число), где 

`k * p <= n`, но `(k + 1) * p > n`, тогда `k = n // p`

Аналогичные рассуждения можно применить для `p ** 2`, `p ** 3` и т.д.

Тогда `key = n // p + n // (p ** 2) + n // (p ** 3) + ... + n // (p ** q)`, где `q = int(log(n, p))`

Автоматизируем расчёты и расшифровку флага:
```python
from binascii import unhexlify
from Crypto.Util.number import long_to_bytes
from pwn import xor
from math import log

p = ...
n = ...
enc_flag = b'...'

enc_flag = unhexlify(enc_flag)

key = 0
for power in range(1, int(log(n, p))):
    key += n // (p ** power)
key = long_to_bytes(key)
flag = xor(enc_flag, key).decode()
flag = flag[:flag.find("}") + 1]
print(flag)
```

Получаем флаг: `MSKCTF{y0ur_br41n_h45_1nf1n173_p374fl0p5}`