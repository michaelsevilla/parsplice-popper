# HEALTH

How do I know ParSplice is working?

- CPU utilization is pinned on the splicer and workers (ranks 0 and > 3).

    ```
    PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND                                                                                 
    17850 root      20   0  306m 106m 6548 R  101  1.3   2:14.87 parsplice                                                                                
    17852 root      20   0  222m  19m 7568 R  101  0.2   2:14.78 driver                                                                                   
    18582 issdm     20   0 17340 1276  904 R    2  0.0   0:00.01 top     
    ```

- Logs on the splicer shows it is broodcasting segments (`out/p*`)

   ```
   # tail -f /parsplice/build/out/p.3.0
   INFO: RANK: 2 INCOMING: 
    type: 3 dbKey: 0 key: 69 source: 2 destination: 2 pending: 0
   INFO: RANK: 2 PROCESSING INCOMING PUT 69 0 
   INFO: RANK: 2 ADDING  0 69 TO STORE 
   INFO: RANK: 2 OUTGOING: 
    type: 3 dbKey: 0 key: 69 source: 2 destination: 1 pending: 0
   SPLICER BROADCASTING
   CURRENT HEAD 69
   SCHEDULING 1 INSTANCES IN STATE 69 FOR WORKER 1
   SCHEDULING 0 INSTANCES IN STATE 69 FOR WORKER 2
   ```

- Logs on the workers shows they are computing segments (`out/p*`)

   ```
   # tail -f out/p.3.0 
   WAITED 662487 ms to process the task
   INFO: WAITED 662487 ms to process the task
   WAITED 0 ms for the push
   INFO: WAITED 0 ms for the push
   WAITED 2 ms for the pull
   INFO: WAITED 2 ms for the pull
   GENERATING SEGMENT 
    INITIAL LABEL: 1658712532116108083    
   ```

This assumes you started up a ParSplice run with directions from
[DEPLOY.md](DEPLOY.md). 

## Visualization

If you are running with my monitoring Docker containers, you can visualize the
performance/utilization metrics:

### Live graphs

While the job is running, point your browser at the head node port 8082 (e.g.,
`http://c220g2-011307.wisc.cloudlab.us:8082/`). Then you can look at any
resource utilization or performance metric. To get the dashboard below, follow
the directions in [DASHBOARD.md](DASHBOARD.md).

![Sevilla Dashboard](figs/live_monitoring.png)

### Post-mortem graphs

When the job finishes, you should have some results directories. We can use
Python Notebooks to visualize the results:

```
cd parsplice/deploy/visualize
./jupyter.sh
```

This will pull a Docker container with Jupyter, the packages for running Python
Notebooks. When it is running, point your browser at the head node port 81
(e.g., `http://c220g2-011307.wisc.cloudlab.us:81/`) and open the file
`visualize/inprogress.ipynb`.
