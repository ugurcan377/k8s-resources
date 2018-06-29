import csv
import json
import shutil

def read_file(data):
    file_tmp = "{srv_key}_{net}_{ins}_{exp}_{conn}.csv"
    print 'Reading {}'.format(file_tmp.format(**data))
    f = open(file_tmp.format(**data))
    res = []
    reader = csv.reader(f)
    for line in reader:
        if line:
            try:
                res.append(float(line[0]) * 100)
            except ValueError:
                pass
    f.close()
    return res
    

def write_as_json(ds, data):
    file_tmp = "{srv_key}_{net}_{ins}_{exp}_{conn}"
    json.dump({"latency": ds}, open("{}.json".format(file_tmp.format(**data)), 'w'))
    shutil.move("{}.csv".format(file_tmp.format(**data)), "csv/{}.csv".format(file_tmp.format(**data)))


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
                write_as_json(ds, metadata)
