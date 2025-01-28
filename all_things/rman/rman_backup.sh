#!/bin/bash

rman target / log='/home/oracle/rman_backup/rman_backup.log' << EOF
run{
    allocate channel ch1 device type disk;

    backup database plus archivelog format '/home/oracle/rman_backup/%d_%s_%U.bkp';

    release channel ch1;

}
exit
EOF

