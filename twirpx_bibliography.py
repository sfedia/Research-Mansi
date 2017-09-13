#!/usr/bin/python3
import bibliography
import json
import time

twirpx_agent = bibliography.Src.Twirpx('*', soft_start = True)

links = open('bibliography/twirpx/files.txt').read().splitlines()

result_table = {}
twirpx_start = 'http://twirpx.com'

index = 0
for link in links:
    print('#{} link is checked'.format(index))
    result = twirpx_agent.analyze_file(twirpx_start + link)
    if result:
        result_table[link] = result
        print('{} added to the result_table'.format(link))
    index += 1
    time.sleep(0.1)

print('OK')

with open('bibliography/twirpx/results.txt', 'w') as result_file:
    result_file.write(json.dumps(result_table))
    result_file.close()

print('file recording finished')