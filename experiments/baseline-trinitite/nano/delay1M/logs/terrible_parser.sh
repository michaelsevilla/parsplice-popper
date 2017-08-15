#!/bin/bash

while [ "$answer" != "yes" ]; do
  read -p "Are you ready for some terrible parsing? [yes/no] " answer
  if [ "$answer" != "yes" ]; then
    echo "Then close your eyes, prepare your body, and refocus. I'll wait 10 seconds..."
    for i in `seq 1 10`; do echo "... $i"; sleep 1; done
  fi
done

set -x
echo "pulling CPU out of log"
cat parsplice.log | grep CPU > cpu.log
cat parsplice.log | grep -v CPU > parsplice.nocpu.log

echo "pulling LABEL out of log"
cat parsplice.nocpu.log | grep LABEL > label.log
cat parsplice.nocpu.log | grep -v LABEL > parsplice.nocpulabel.log
rm parsplice.nocpu.log

echo "pulling SemanticPerf out of log"
cat parsplice.nocpulabel.log | grep SemanticPerf > perf.log
cat parsplice.nocpulabel.log | grep -v SemanticPerf > rest.log
rm parsplice.nocpulabel.log

for metric in "cpu" "label" "perf" "rest"; do
  for node in `seq 0 31`; do
    if [ $node -lt 10 ]; then
      name="0$node"
    else
      name="$node" 
    fi

    cat ${metric}.log | grep "^${name}:" > ${metric}.${name}.log
    tar czf ${metric}.${name}.tar.gz ${metric}.${name}.log
    rm ${metric}.${name}.log
    echo "... splitting $metric for node $name"
  done
  rm ${metric}.log
done
