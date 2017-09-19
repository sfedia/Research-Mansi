import os
import re
import time

mian_len = -1
maan_len = -1

while True:

    ignore = ['~', 'stats']
    ld = os.listdir('.')
    inds = {}

    for ld_el in ld:
        if re.search('^(' + '|'.join(ignore) + ')', ld_el):
            continue
        name = re.sub('-\d+$', '', ld_el)
        if not name in inds:
            inds[name] = 1
        else:
            inds[name] += 1

    inds_rev = {}
    all_nums = []

    for i in inds:
        if not inds[i] in inds_rev:
            inds_rev[inds[i]] = []
        all_nums.append(inds[i])
        inds_rev[inds[i]].append(i)
    print(mian_len, maan_len)
    if len(inds_rev[min(all_nums)]) != mian_len or len(inds_rev[max(all_nums)]) != maan_len:
        with open('stats.txt', 'w') as stats_file:
            mian_len = len(inds_rev[min(all_nums)])
            maan_len = len(inds_rev[max(all_nums)])
            output = str(min(all_nums)) + " : " + ', '.join(inds_rev[min(all_nums)])
            output += "\n\n"
            output += str(max(all_nums)) + " : " + ', '.join(inds_rev[max(all_nums)])
            stats_file.write(output)
            stats_file.close()

    time.sleep(0.2)


