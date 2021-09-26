import math
from pwn import remote


def solve(x1, y1, x2, y2, x3, y3):
    cosC = ((x1 - x3) * (x2 - x3) + (y1 - y3) * (y2 - y3)) / (((x1 - x3) ** 2 + (y1 - y3) ** 2) ** 0.5 * ((x2 - x3) ** 2 + (y2 - y3) ** 2) ** 0.5)
    cosA = ((x2 - x1) * (x3 - x1) + (y2 - y1) * (y3 - y1)) / (((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 * ((x3 - x1) ** 2 + (y3 - y1) ** 2) ** 0.5)
    cosB = ((x1 - x2) * (x3 - x2) + (y1 - y2) * (y3 - y2)) / (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 * ((x3 - x2) ** 2 + (y3 - y2) ** 2) ** 0.5)
    return [round(math.degrees(math.acos(cosA)), 2), round(math.degrees(math.acos(cosB)), 2), round(math.degrees(math.acos(cosC)), 2)]


r = remote('62.84.118.87', 9004)

for i in range(49):
    r.recvuntil("Раунд".encode())
    values = list(map(float, r.recvline().strip().decode().split(";")))
    answer = list(map(str, solve(*values)))
    answer = ";".join(answer)
    r.sendline(answer.encode())
r.interactive()
