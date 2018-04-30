import json

from tabulate import tabulate


scheme1 = ((1, 1, 1), (10, 1, 1), (25, 1, 1), (50, 1, 1), (75, 1, 1), (100, 1, 1))


def parse_dict(source, query):
    template = ".get('{}', {{}})"
    cmd = "source"
    for q in query.split("/"):
        if '#' in q:
            q = q.replace('#', '')
            cmd += template.format(q) + "[0]"
        else:
            cmd += template.format(q)
    try:
        return eval(cmd) or 0
    except KeyError:
        return 0


def get_raw_data(req, node, scheme, count, net, srv, thres):
    fn_template="{thres}/{srv}_{net}_{node}_{g}_{l}_{s}_{count}_{req}.json"
    arg_dict = {"srv": srv, "net": net, "g": scheme[0], "l": scheme[1], 
    "s": scheme[2], "node": node, "req": req, "count": count, "thres": thres}
    return json.loads(json.load(open(fn_template.format(**arg_dict))))


def get_result(queries, req, node, scheme, exp_count, net, srv, thres):
    gls = "{}_{}_{}".format(*scheme)
    result = [net, req, srv, "{}_{}".format(node, gls), thres[0], exp_count]
    data = get_raw_data(req, node, scheme, exp_count, net, srv, thres[1])
    for query in queries:
        result.append(parse_dict(data, query))
    return result

results = []
net_list = ["flannel", "calico", "weave"]
node_list = [2]
req_list = [10000, 30000, 50000, 80000, 100000]
scheme = scheme1
exp_count = 3
thresholds = ((10, "ten"), (15, "fifteen"), (20, "twenty"))
srv = "g"
q = ["result/latency/mean"]
headers = ["Network", "Request #", "Srv", "Instances", "Thr","Exp #", "Mean Lat"]

for net in net_list:
    for node in node_list:
        for req in req_list:
            for sch in scheme:
                for exp in range(1, exp_count+1):
                    for thres in thresholds:
                        results.append(get_result(q, req, node, sch, exp, net, srv, thres))


print(tabulate(results, headers=headers))
