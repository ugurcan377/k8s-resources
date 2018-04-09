"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars.
"""
import json

import numpy as np
import matplotlib.pyplot as plt


KeyakiGreen = '#4ab14b'
scheme1 = ((1, 1, 1), (10, 1, 1), (25, 1, 1), (50, 1, 1), (75, 1, 1), (100, 1, 1))
scheme2 = ((1, 1, 1), (5, 5, 1), (12, 12, 1), (25, 25, 1), (50, 50, 1)) # , (60, 60, 1)


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


def get_file_list(req, node, scheme, net='bridge'):
    file_list = []
    fn_template="{srv}_{net}_{node}_{g}_{l}_{s}_{req}.json"
    for g, l, s in scheme:
        arg_dict = {"srv": "g", "net": net, "g": g, "l": l,
                    "s": s, "node": node, "req": req}
        g_file = fn_template.format(**arg_dict)
        arg_dict["srv"] = "l"
        l_file = fn_template.format(**arg_dict)
        arg_dict["srv"] = "s"
        s_file = fn_template.format(**arg_dict)
        file_list.append((g_file, l_file, s_file))
    return file_list


def get_raw_data(fname):
    return json.loads(json.load(open(fname)))


def prepare_datasource(file_list, query):
    g_ds = []
    l_ds = []
    s_ds = []
    for gf, lf, sf in file_list:
        g_data = get_raw_data(gf)
        g_ds.append(parse_dict(g_data, query))
        l_data = get_raw_data(lf)
        l_ds.append(parse_dict(l_data, query))
        s_data = get_raw_data(sf)
        s_ds.append(parse_dict(s_data, query))
    return g_ds, l_ds, s_ds


def bar_chart(ds1, ds2, ds3, scheme, metadata):

    ind = np.arange(len(ds1))  # the x locations for the groups
    width = 0.27  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width , ds1, width, color= KeyakiGreen, label='G')
    rects2 = ax.bar(ind , ds2, width, color='SkyBlue', label='L')
    rects3 = ax.bar(ind + width , ds3, width, color='IndianRed', label='S')

    def autolabel(rects, index, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

        for i, rect in enumerate(rects):
            ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1,
                    '{}'.format(scheme[i][index]), ha=ha[xpos], va='bottom')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(metadata['chart']['x'])
    ax.set_xlabel(metadata['chart']['y'])
    ax.set_xticklabels([])
    ax.set_title(metadata['chart']['title'].format(**metadata))
    ax.legend()

    autolabel(rects1, 0, "center")
    autolabel(rects2, 1, "center")
    autolabel(rects3, 2, "center")

    plt.savefig(open("figures/{exp}_{net}_{node}_{req}_s{scheme}.png".format(**metadata), 'w'))

def all_charts(query, exp, chart_meta):
    net_list = ["bridge"]
    node_list = [1]
    req_list = [100, 1000, 10000, 50000, 100000]
    scheme_list = [scheme1, scheme2]
    for net in net_list:
        for node in node_list:
            for req in req_list:
                for i,scheme in enumerate(scheme_list):
                    try:
                        fl = get_file_list(req, node, scheme)
                        ds1, ds2, ds3 = prepare_datasource(fl, query)
                        bar_chart(ds1, ds2, ds3, scheme, {
                            "net": net, "node": node, "req": req, "scheme": i+1, "exp": exp, "chart": chart_meta})
                    except IOError as e:
                        print e


all_charts("result/latency/mean", "meanlat", {
    'x': "Latency (us)", "y": "Instance count",
    "title": "Mean Latency for {net} Network {node} Nodes {req} Requests"})
