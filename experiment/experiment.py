import click
import delegator
import json
import time


def run_exp(net, exp_str):
    servers = {
    "g": "http://10.192.0.3:32223",
    "l": "http://10.192.0.3:32224",
    "s": "http://10.192.0.3:32225",
    }
    tests = [(20, 10000), (40, 30000), (60, 50000), (80, 80000), (100, 100000)]
    cmd_template = "bombardier -c {conn} -n {req} -p r -o json {srv}"
    for srv_key,srv in servers.iteritems():
        for conn, req in tests:
            print "Running {} with {}/{}".format(srv_key, conn, req)
            cmd = cmd_template.format(conn=conn, req=req, srv=srv)
            res = delegator.run(cmd)
            json.dump(res.out, open("{srv_key}_{net}_{exp_str}_{req}.json".format(
                srv_key=srv_key, net=net, exp_str=exp_str, req=req), "w"))


@click.command()
@click.option("--net")
@click.option("--node")
@click.option("--exp")
def run_auto(net, node, exp):
    scale_template = "kubectl scale deploy/{selection} --replicas={count}"
    status_template = 'kubectl get deploy/{selection} -o json'
    schemes = (((1, 1, 1), (10, 1, 1), (25, 1, 1), (50, 1, 1), (75, 1, 1), (100, 1, 1)),
    ((1, 1, 1), (5, 5, 1), (12, 12, 1), (25, 25, 1), (37, 37, 1), (50, 50, 1)))
    experiments = int(exp)
    for exp in range(1,experiments+1):
        print 'Starting Experiment #{}'.format(exp)
        for scheme in schemes:
            for g, l, s in scheme:
                print 'Starting experiment {} for {}/{}/{}/{}/{}'.format(exp, net, node, g, l, s)
                delegator.run(scale_template.format(selection='garasu', count=g))
                delegator.run(scale_template.format(selection='lat', count=l))
                delegator.run(scale_template.format(selection='startdash', count=s))
                cycle = 0
                while True:
                    g_dict = json.loads(delegator.run(status_template.format(selection='garasu')).out)
                    l_dict = json.loads(delegator.run(status_template.format(selection='lat')).out)
                    s_dict = json.loads(delegator.run(status_template.format(selection='startdash')).out)
                    g_check = g_dict['status']['availableReplicas'] == g
                    l_check = l_dict['status']['availableReplicas'] == l
                    s_check = s_dict['status']['availableReplicas'] == s
                    if g_check and l_check and s_check:
                        print 'Scaling for {}/{}/{} took {} seconds'.format(g, l, s, cycle * 10)
                        break
                    else:
                        cycle += 1
                        time.sleep(10)
                run_exp(net, '{}_{}_{}_{}_{}'.format(node, g, l, s, exp))

run_auto()
