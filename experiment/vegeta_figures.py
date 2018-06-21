import json
import os

import click
import numpy as np
import matplotlib.pyplot as plt


scheme1 = range(10, 81, 5)


def parse_dict(source, query):
    template = ".get('{}', {{}})"
    cmd = "source"
    for q in query.split("/"):
        cmd += template.format(q)
    try:
        return eval(cmd) or 0
    except KeyError:
        return 0


def file_list_by_scheme(scheme, srv, net, count, conn):
    file_list = []
    fn_template="{srv}_{net}_{g}_{count}_{conn}.json"
    for g in scheme:
        arg_dict = {"srv": srv, "net": net, "g": g, "conn": conn, "count": count}
        g_file = fn_template.format(**arg_dict)
        file_list.append(g_file)
    return file_list


def file_list_by_conn(srv_count, srv, net, count, conn_list):
    file_list = []
    fn_template="{srv}_{net}_{g}_{count}_{conn}.json"
    for conn in conn_list:
        arg_dict = {"srv": srv, "net": net, "g": srv_count, "conn": conn, "count": count}
        g_file = fn_template.format(**arg_dict)
        file_list.append(g_file)
    return file_list


def get_raw_data(fname):
    res = json.load(open(fname))
    if type(res) == unicode:
        return json.loads(res)
    else:
        return res


def prepare_datasource(file_list, query):
    g_ds = []
    for gf in file_list:
        g_data = get_raw_data(gf)
        g_ds.append(parse_dict(g_data, query) / float(10 ** 6))
    return g_ds


def chart(ds_list, scheme, metadata):
    for q, ds in ds_list:
        plt.plot(np.array(scheme), np.array(ds), label=q)
        
    plt.ylabel(metadata['chart']['x'])
    plt.xlabel(metadata['chart']['y'])
    plt.title(metadata['chart']['title'].format(**metadata))
    plt.legend()
    dir_tmp = "figures/{srv}_{conn}"
    if not os.path.exists(dir_tmp.format(**metadata)):
        os.makedirs(dir_tmp.format(**metadata))
    plt.savefig(open("figures/{srv}_{conn}/{ename}_{exp}_{srv}_{conn}_s{scheme}.png".format(**metadata), 'w'))
    plt.clf()


def charts_by_scheme(ename, exp_count, chart_meta):
    net_list = ["flannel"]
    scheme = [scheme1]
    srv = 'g'
    conn_list = range(100, 2001, 50)
    query_list = ["mean", "50th", "95th", "99th","max"]
    query_tmp = "latencies/{}"
    for net in net_list:
        for conn in conn_list:
            for sch in scheme:
                try:
                    fl1 = file_list_by_scheme(sch, srv, net, exp_count, conn)
                    ds_list = []
                    for q in query_list:
                        ds_list.append((q, prepare_datasource(fl1, query_tmp.format(q))))
                    chart(ds_list, sch, {
                        "net": net, "conn": conn, "scheme": 1,
                        "exp": exp_count, "srv": srv, "chart": chart_meta, 'ename': ename})
                except IOError as e:
                    print e


def charts_by_conn(ename, exp_count, chart_meta):
    net = chart_meta['net']
    sch = chart_meta['setup'][1]
    srv = chart_meta['setup'][0]
    conn_list = range(*chart_meta['step'])
    query_list = chart_meta["queries"]
    for exp in range(1, exp_count+1):
        try:
            fl1 = file_list_by_conn(sch, srv, net, exp, conn_list)
            for q in query_list:
                ds_list = []
                ds_list.append((q, prepare_datasource(fl1, q)))
                chart(ds_list, conn_list, {
                    "net": net, "conn": sch, "scheme": 1,
                    "exp": exp, "srv": srv, "chart": chart_meta, "sch": sch, 'ename': q})
        except IOError as e:
            print e


def avg_charts_by_conn(ename, exp_count, chart_meta):
    net = chart_meta['net']
    sch = chart_meta['setup'][1]
    srv = chart_meta['setup'][0]
    conn_list = range(*chart_meta['step'])
    query_list = chart_meta["queries"]
    try:
        mean = lambda res: [sum(k)/len(k) for k in zip(*res)]
        for q in query_list:
            ds_list = []
            exp_list = []
            for exp in range(1, exp_count+1):
                fl1 = file_list_by_conn(sch, srv, net, exp, conn_list)
                exp_list.append(prepare_datasource(fl1, q))
            ds_list.append((q, mean(exp_list)))
            chart(ds_list, conn_list, {
                "net": net, "conn": sch, "scheme": 1,
                "exp": exp, "srv": srv, "chart": chart_meta, "sch": sch, 'ename': "{}_avg".format(q)})
    except IOError as e:
        print e
        

@click.command()
@click.option('--ctype', type=click.Choice(['scheme', 'conn', 'avgconn']), default='avgconn')
@click.option('--exp', default=1)
@click.option('--ename', default='subete')
@click.option('--setup', type=(unicode, int))
@click.option('--step', type=(int, int, int), default=(100, 4001, 100))
@click.option('--net', type=click.Choice(['flannel', 'calico', 'weave']), default='flannel')
@click.option('--alt-query', is_flag=True)
def charts(ctype, exp, ename, setup, step, net, alt_query):
    queries = ["latencies/mean", "latencies/50th", "latencies/95th", "latencies/99th",
     "latencies/max"]
    if alt_query:
        queries = ["result/latency/mean", "result/rps/percentile/50", "result/rps/percentile/75",
         "result/rps/percentile/90",  "result/rps/percentile/95",  "result/rps/percentile/99",
         "result/latency/max"]
    meta_data = {'x': "Latency (ms)", "y": "", "title": "", "setup": setup, "step": step,
     "net": net, "queries": queries}
    
    if ctype == 'scheme':
        meta_data['y'] = "Instance count"
        meta_data['title'] = "Latency for {srv} Server {conn} Connections"
        charts_by_scheme(ename, exp, meta_data)
        
    if ctype in ['conn', 'avgconn']:
        meta_data['y'] = 'Connection count'
        meta_data['title'] = "Latency for {srv} Server {sch} Instances"
        if ctype == 'conn':
            charts_by_conn(ename, exp, meta_data)
        if ctype == 'avgconn':
            avg_charts_by_conn(ename, exp, meta_data)


charts()
