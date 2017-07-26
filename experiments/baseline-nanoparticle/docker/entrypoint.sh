#!/bin/bash
# Stolen from https://raw.githubusercontent.com/ivotron/docker-openmpi/master/mpirun_docker
set -ex
if [ -z "$RANK0" ] ; then
  # if we are not RANK0, we just launch sshd
  /root/.ssh/entrypoint.sh
  exit 0
fi

# else we are the head node
if [ ! -f /tmp/mpihosts ]; then
  echo "Expecting /tmp/mpihosts file"
  exit 1
fi

# send sshd to background
/root/.ssh/entrypoint.sh &> /dev/null &

# start pbs
HOSTNAME=`hostname`
echo "127.0.0.1 $HOSTNAME" >> /etc/hosts
echo $HOSTNAME > /etc/torque/server_name
echo "$HOSTNAME np=4" > /var/spool/torque/server_priv/nodes && \
echo "$HOSTNAME" > /var/spool/torque/mom_priv/config && \
echo "$HOSTNAME" > /etc/torque/server_name && \
echo "$HOSTNAME" > /var/spool/torque/server_priv/acl_svr/acl_hosts && \
echo root@$HOSTNAME > /var/spool/torque/server_priv/acl_svr/operators && \
echo root@$HOSTNAME > /var/spool/torque/server_priv/acl_svr/managers

# start torque
/etc/init.d/torque-server start
/etc/init.d/torque-mom start
sleep 5
qmgr -c 'set server scheduling = true'
qmgr -c 'set server keep_completed = 300'
qmgr -c 'set server mom_job_sync = true'
qmgr -c 'create queue batch'
qmgr -c 'set queue batch queue_type = execution'
qmgr -c 'set queue batch started = true'
qmgr -c 'set queue batch enabled = true'
qmgr -c 'set queue batch resources_default.walltime = 1:00:00'
qmgr -c 'set queue batch resources_default.nodes = 1'
qmgr -c 'set server default_queue = batch'
qmgr -c 'set server submit_hosts = SERVER'
qmgr -c 'set server allow_node_submit = true'
qmgr -c 's s acl_roots+=root@*'

/bin/bash -c "$@"
