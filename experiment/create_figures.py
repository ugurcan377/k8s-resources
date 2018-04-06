"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars.
"""
import numpy as np
import matplotlib.pyplot as plt

scheme1 = ((1, 1, 1), (10, 1, 1), (25, 1, 1), (50, 1, 1), (100, 1, 1))
scheme2 = ((1, 1, 1), (5, 5, 1), (12, 12, 1), (25, 25, 1), (50, 50, 1), (60, 60, 1))


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


def bar_chart(fname, ds1, ds2, ds3, scheme):

    ind = np.arange(len(ds1))  # the x locations for the groups
    width = 0.25  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width , ds1, width, color='#4ab14b', label='G')
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
                    '{}'.format(scheme[index][i]), ha=ha[xpos], va='bottom')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Latency (ms)')
    ax.set_xlabel('Instance count')
    ax.set_xticklabels([])
    ax.set_title('Latency by instance count')
    ax.legend()

    autolabel(rects1, 0, "center")
    autolabel(rects2, 1, "center")
    autolabel(rects3, 2, "center")

    plt.show()
    #plt.savefig(open("{}.png".format(fname)))

men_means, men_std = (20, 35, 30, 35, 27), (2, 3, 4, 1, 2)
women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)
inter_means = (25, 32, 34, 20, 25)

bar_chart('', men_means, women_means, inter_means, scheme1)
print get_file_list(100, 1, scheme1)