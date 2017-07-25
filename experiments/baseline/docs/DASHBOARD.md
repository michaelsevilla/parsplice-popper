# DASHBOARD

To get the dashboard I like looking at for ParSplice, browse to the head node
port 8082 (e.g., `http://c220g2-011307.wisc.cloudlab.us:8082/dashboard`), click
`Dashboard->Edit Dashboard` and paste in some variant of the below
(substituting your CloudLab hostnames):

```json
[
  {
    "target": [
      "node-1.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.leveldb.ApiWrite",
      "node-1.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.leveldb.ApiDelete"
    ],
    "lineMode": "connected",
    "title": "Database Writes",
    "hideLegend": "true"
  },
  {
    "target": [
      "node-0.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.cputotals.user",
      "node-1.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.cputotals.user",
      "node-3.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.cputotals.user"
    ],
    "title": "Splicer/DB/InMemoryDB CPU (user)",
    "lineMode": "connected"
  },
  {
    "target": [
      "node-4.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.cputotals.user",
      "node-5.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.cputotals.user",
      "node-6.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.cputotals.user",
      "node-7.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.cputotals.user",
      "node-8.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.cputotals.user"
    ],
    "title": "Worker CPU (user)",
    "lineMode": "connected",
    "hideLegend": "true"
  },
  {
    "target": [
      "node-1.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.leveldb.ApiOpen",
      "node-1.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.leveldb.ApiGet"
    ],
    "lineMode": "connected",
    "title": "Database Reads",
    "hideLegend": "true"
  },
  {
    "target": [
      "scale(node-0.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.meminfo.used,1024)",
      "scale(node-3.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.meminfo.used,1024)",
      "scale(node-1.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.meminfo.used,1024)"
    ],
    "title": "Splicer/DB/InMemoryDB Memory (used)",
    "hideLegend": "false",
    "drawNullAsZero": "true"
  },
  {
    "target": [
      "scale(node-4.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.meminfo.used,1024)",
      "scale(node-5.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.meminfo.used,1024)",
      "scale(node-6.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.meminfo.used,1024)",
      "scale(node-7.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.meminfo.used,1024)",
      "scale(node-8.msevilla-qv27256.cephfs-pg0.wisc.cloudlab.us.meminfo.used,1024)"
    ],
    "title": "Worker Memory (used)",
    "hideLegend": "true",
    "lineMode": "connected"
  }
]
```
