import json

from tabulate import tabulate

def read_file(data):
    file_tmp = "{srv_key}_{net}_{ins}_{exp}_{conn}.json"
    f = open(file_tmp.format(**data))
    res = json.load(f)
    f.close()
    return res['latency']
    
def calculate_results(ds):
    res_dict = {}
    ds.sort()
    res_dict['max'] = ds[-1]
    res_dict['mean'] = sum(ds)/len(ds)
    ds_len = len(ds) / 100
    res_dict['50th'] = ds[ds_len * 50]
    res_dict['75th'] = ds[ds_len * 75]
    for i in range(90, 100):
        res_dict['{}th'.format(i)] = ds[ds_len * i]
    return res_dict

results = {}
net_list = ["flannel"]
srv_dict = {"sm": 40, 'g': 20, 'la': 10, "ml": 4, "super": 2}
conn_list = range(100, 4001, 100)
exp_count = 8

for net in net_list:
    for srv in srv_dict.keys():
        for exp in range(1, exp_count+1):
            for conn in conn_list:
                metadata = {"srv_key": srv, "net": net, "conn": conn, "ins": srv_dict[srv], "exp": exp}
                ds = read_file(metadata)
                exp_str = "{srv_key}_{net}_{ins}_{exp}_{conn}".format(**metadata)
                print(exp_str)
                results[exp_str] = calculate_results(ds)
                results[exp_str]['exp_time'] = open("time/{}".format(exp_str)).read().strip()
                
json.dump(results, open("2hey_results.json", 'w'))
