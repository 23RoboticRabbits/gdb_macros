# gdb_macros

#lwlocks.py

When you suspect a problem with LWLocks, please perform the following:

Generate a core file of any process waiting on locks and then collect it using packcore:
gcore <PID>

In a empty directory, run this script to dump stacks and held locks for all postgres processes on the server.

#!/bin/bash
unset PYTHONHOME
unset LD_LIBRARY_PATH
GDB=/usr/bin/gdb
ps -o state,uid,pid,ppid,c,pri,ni,rss,sz,wchan=WIDE-WCHAN-COLUMN,stime,tty,time,cmd -Cpostgres > dumps.ps
for proc in $(ps -flyCpostgres --no-heading | awk '{print $3}')
do
    $GDB --batch -ex "print held_lwlocks" -ex "thread apply all bt" /proc/$proc/exe $proc > dumps.$proc
    echo "" >> dumps.$proc
    cat /proc/$proc/stack >> dumps.$proc
done

If you have the knowledge to debug the above outputs then make an attempt to debug. If not then the process which is waiting on the lock should be terminated using usual methods.

Download and then execute the following inside gdb:
(gdb) source /path/to/lwlocks.py
(gdb) dump-lwlock-array

# Batch Example
cat << EOF >> gdb.commands
thread apply all bt
source /path/to/lwlocks.py
dump-lwlock-array
q
EOF


ps -C postgres -o pid --no-heading | while read pid; do ps -p $pid -o pid,command | tee gdb.$pid.out; gdb /usr/local/greenplum-db/bin/postgres -p $pid < gdb.commands >> gdb.$pid.out; done
