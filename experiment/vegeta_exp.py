import click
import delegator
import json
import time


def run_exp(net, exp_str, srv_key, hey=False):
    servers = {
    "g": "http://10.192.0.3:32223",
    "l": "http://10.192.0.3:32224",
    "s": "http://10.192.0.3:32225",
    "super": "http://10.192.0.3:32226",
    "xl": "http://10.192.0.3:32227",
    "ml": "http://10.192.0.3:32228",
    "sm": "http://10.192.0.3:32229",
    "la": "http://10.192.0.3:32230",
    }
    tests = range(100, 4001, 100)
    if hey:
        cmd_template = "hey -o csv -c {rps} -z {dur} {srv} > {result}.csv"
    else:
        cmd_template = "echo 'GET {srv}' | vegeta attack -duration={dur} -rate={rps} |\
        vegeta report -reporter=json > {result}.json"
    dur = "2m"
    srv = servers[srv_key]
    for conn in tests:
        print "Running {} with {}".format(srv_key, conn)
        res = "{srv_key}_{net}_{exp_str}_{req}".format(
            srv_key=srv_key, net=net, exp_str=exp_str, req=conn)
        cmd = cmd_template.format(conn=conn, srv=srv, dur=dur, rps=conn, result=res)
        tfile = open("time/{srv_key}_{net}_{exp_str}_{req}".format(
            srv_key=srv_key, net=net, exp_str=exp_str, req=conn), "w")
        tfile.write(time.ctime())
        tfile.close()
        res = delegator.run(cmd)


@click.command()
@click.option("--net")
@click.option("--exp")
@click.option('--setup', type=(unicode, int))
@click.option('--start', default=1)
@click.option('--hey', is_flag=True)
def run_auto(net, exp, setup, start, hey):
    deployments = {
        "g": "garasu",
        "l": "lat",
        "s": "startdash",
        "super": "supergarasu",
        "xl": "xlgarasu",
        "ml": "mlgarasu",
        "sm": "small",
        "la": "large",
    }
    scale_template = "kubectl scale deploy/{selection} --replicas={count}"
    status_template = 'kubectl get deploy/{selection} -o json'
    schemes = [setup[1]]
    experiments = int(exp)
    deploy = deployments[setup[0]]
    for exp in range(start,experiments+1):
        print 'Starting Experiment #{}'.format(exp)
        for g in schemes:
            print 'Starting experiment {} for {}/{}'.format(exp, net, g)
            delegator.run(scale_template.format(selection=deploy, count=g))
            cycle = 0
            while True:
                g_dict = json.loads(delegator.run(status_template.format(selection=deploy)).out)
                if g_dict['status']['availableReplicas'] == g:
                    print 'Scaling for {} took {} seconds'.format(g, cycle * 10)
                    break
                else:
                    cycle += 1
                    time.sleep(10)
            run_exp(net, '{}_{}'.format(g, exp), setup[0], hey)
    delegator.run(scale_template.format(selection=deploy, count=1))

run_auto()
