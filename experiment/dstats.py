import json
import re

regex = re.compile('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* Container=([a-z0-9]{12}) .* CPU=(\d{1,})')
results = {}

f1 = open('docker.txt')
f2 = open('docker2.txt')

def get_cpu_usage(fp):
    for line in fp.readlines():
        match = regex.match(line)
        if match:
            t, cont_id, cpu = match.group(1, 2, 3)
            if results.get(cont_id):
                results[cont_id].append((t, cpu))
            else:
                results[cont_id] = [(t, cpu)]
    fp.close()
            
get_cpu_usage(f1)
get_cpu_usage(f2)

json.dump(results, open('docker_stats.json', 'w'))
