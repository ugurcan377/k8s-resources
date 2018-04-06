import click
import delegator
import json

@click.command()
@click.option("--net")
@click.option("--exp-str") #exp-str should be node_garasu_lat_startdash
def run_exp(net, exp_str):
    servers = {
    "g": "http://10.192.0.3:32223",
    "l": "http://10.192.0.3:32224",
    "s": "http://10.192.0.3:32225",
    }
    tests = [(10, 100), (25, 1000), (50, 10000), (75, 50000), (100, 100000)]
    cmd_template = "bombardier -c {conn} -n {req} -p r -o json {srv}"
    for srv_key,srv in servers.iteritems():
        for conn, req in tests:
            print "Running {} with {}/{}".format(srv_key, conn, req)
            cmd = cmd_template.format(conn=conn, req=req, srv=srv)
            res = delegator.run(cmd)
            json.dump(res.out, open("{srv_key}_{net}_{exp_str}_{req}.json".format(
                srv_key=srv_key, net=net, exp_str=exp_str, req=req), "w"))
                
run_exp()
