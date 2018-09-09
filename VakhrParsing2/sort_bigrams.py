#!/usr/bin/python3

#import matplotlib.pyplot
from itertools import product


dict_alph = [
    "Ааӓ", "Бб", "Вв", "Гг", "Дд", "ЕеЁё", "Жж", "Зз", "Ии", "Йй", "Кк", "Лл", "Мм", "Нн", "Ӈӈ",
    "ОоӦӧӨө", "Пп", "Рр", "Сс", "Тт", "УуӰӱ", "Фф", "Хх", "Цц", "Чч", "Шш", "Щщ", "Ъъ", "Ыы", "Ьь", "Ээ", "Юю", "Яя",
    "әӛ"
]

lines = open('balandin_vakhr.txt', 'r', encoding='utf-8').read().splitlines()

rows = []
address_index = {}


class BigramRow:
    def __init__(self, addr, count=1):
        self.address = addr
        self.count = count
        self.index = -1


def get_char_address(char):
    for n, group in enumerate(dict_alph):
        if char in group:
            return n
    raise ValueError()


for line in lines:
    if len(line) < 2:
        continue
    bigram_address = []
    for x in range(2):
        try:
            bigram_address.append(get_char_address(line[x]))
        except ValueError:
            continue
    if not rows:
        rows.append(BigramRow(bigram_address))
    else:
        if rows[-1].address == bigram_address:
            rows[-1].count += 1
        else:
            rows.append(BigramRow(bigram_address))

for i in range(len(rows)):
    rows[i].index = i

for address in product(range(len(dict_alph)), repeat=2):
    g1 = [b_row for b_row in rows if b_row.address == list(address)]
    if not g1:
        continue
    g2 = sorted(g1, key=lambda r: r.count, reverse=True)
    address_index[address] = g2[0].index

arrayed_addresses = sorted(address_index.items(), key=lambda kv: kv[1])
arrayed_addresses = [kv[0] for kv in arrayed_addresses]
max_array_distance = 3

arrayed_addresses = [
    a for k, a in enumerate(arrayed_addresses) if not k or abs(a[0]-arrayed_addresses[k-1][0]) <= max_array_distance
]

dist_aa = []
for k, a in enumerate(arrayed_addresses):
    if not k or abs(a[0]-dist_aa[-1][0]) <= max_array_distance:
        dist_aa.append(a)

print(arrayed_addresses)
print(dist_aa)
