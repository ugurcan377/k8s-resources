# Environment
The cluster: Kubernetes 1.9.6 DinD
Application: MPEG-DASH video streaming
Setup: There are 3 different music videos in DASH format. Video files are served via Nginx web
server and displayed by reference video player dash.js.  
Each video is a seperate Kubernetes Deployment and served by a NodePort Service.

# Experiment Design
There are 4 basic parameters in my experiment. Node count, deployment instance counts for 1st, 2nd
and 3rd deployment. I intend to select a fifth parameter as which networking setup the cluster uses.
For now it's default Linux bridges.

I used [bombardier](https://github.com/codesenberg/bombardier) http load testing tool for sending
requests to these servers and measuring latency. These tool can send n amount of requests from m
amount of connections. The n and m values that I used are provided below.

In each step I changed instance counts for any deployment I ran these tests for each video with an
automated script you can find as experiment.py this script runs these tests and save their results
as json files. Naming scheme for this file are the following.
`(g|l|s)_network_nodeCount_gInstanceCount_lInstanceCount_sInstanceCount_requestCount`
Note: letters g,l and s are considered deployment names. They're first letters of their respective 
songs

## Load Test Values

| Connection # | Request # |
| ------------ | ---------:|
| 10           | 100       |
| 25           | 1000      |
| 50           | 10000     |
| 75           | 50000     |
| 100          | 100000    |

## Testing scheme 

| Node #  | G Server # | L Server # | S Server # |
| ------- |:----------:|:----------:| ----------:|
| 1       | 1          | 1          | 1          |
| 1       | 10         | 1          | 1          |
| 1       | 25         | 1          | 1          |
| 1       | 50         | 1          | 1          |
| 1       | 75         | 1          | 1          |
| 1       | 100        | 1          | 1          |
| 1       | 5          | 5          | 1          |
| 1       | 12         | 12         | 1          |
| 1       | 25         | 25         | 1          |
| 1       | 50         | 50         | 1          |
| 1       | 60         | 60         | 1          |
| 2       | 1          | 1          | 1          |
| 2       | 10         | 1          | 1          |
| 2       | 25         | 1          | 1          |
| 2       | 50         | 1          | 1          |
| 2       | 75         | 1          | 1          |
| 2       | 100        | 1          | 1          |
| 2       | 5          | 5          | 1          |
| 2       | 12         | 12         | 1          |
| 2       | 25         | 25         | 1          |
| 2       | 50         | 50         | 1          |
| 2       | 60         | 60         | 1          |

# Observations During Experiments
- Cluster is running on docker. Therefore nodes have full access the hosts computing resources.
- Since all nodes have the same resources. I didn't expected the number of pods the cluster can run
wouldn't change despite how many nodes were available. That wasn't the case.
- In single node in this setup supported a maximum 103-104 pods. Kubernetes didn't scheduled any more
pods into the after that point. Using a second node solve this problem. But after 120 pods host was
barely responsive. The main bottleneck was the CPU. That was hardly a surprise because it was an fairly
old Intel i7 920.
- Because the benchmark tool and cluster were running on the same machine. This might impact the
container performance. Since same software runs the same tests for all cases I don't think that
compromised the tests reliablity.
- I refrained from using the host machine during tests to alleviate shared resources issue.
