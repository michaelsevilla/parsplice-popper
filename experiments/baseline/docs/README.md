# baseline

Please modify everything in `conf/` to match your cluster:

- `vars.yml`: cluster and simulation variables
- `hosts`: participating nodes
- `mpihosts`: rank order
- `leveldb_metrics`: which operations to monitor

These scripts run the jobs:

- `run.sh`: cleans up, starts parsplice, and starts monitoring
- `repull.sh`: force pulls Docker image



[![Popper Status](http://ci.falsifiable.us/michaelsevilla/hxhim-mantle/baseline/status.svg)](http://falsifiable.us)
