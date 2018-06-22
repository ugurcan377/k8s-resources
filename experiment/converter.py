import os
import shutil

import click

def convert(prefix, expc):
    schemes = (((1, 1, 1), (10, 1, 1), (25, 1, 1), (50, 1, 1), (75, 1, 1), (100, 1, 1)),
        ((1, 1, 1), (5, 5, 1), (12, 12, 1), (25, 25, 1), (37, 37, 1), (50, 50, 1)))
    req_dict = {10000: 20, 30000: 40, 50000: 60, 80000: 80, 100000: 100}
    servers = ['g', 'l', 's']
    net_list = ['flannel', 'calico', 'weave']

    for net in net_list:
        for i, scheme in enumerate(schemes):
            scheme_path = '{}/scheme{}'.format(prefix, i+1)
            if not os.path.exists(scheme_path):
                os.makedirs(scheme_path)
            for sch in scheme:
                for exp in range(1, expc+1):
                    for srv_in, srv in enumerate(servers):
                        for req, conn in req_dict.iteritems():
                            metadict = {"srv": srv, "net": net, "g": sch[0], "l": sch[1],
                             "s": sch[2], "exp": exp, "req": req, "conn": conn, "sch": i+1,
                             "current": sch[srv_in], "prefix": prefix}
                            src = '{prefix}/{srv}_{net}_2_{g}_{l}_{s}_{exp}_{req}.json'.format(**metadict)
                            dst = "{prefix}/scheme{sch}/{srv}_{net}_{current}_{exp}_{conn}.json".format(**metadict)
                            shutil.copy(src, dst)

@click.command()
@click.argument('prefix')
@click.option('--exp', default=10)
def converter(prefix, exp):
    convert(prefix, exp)
    

converter()
