#!/usr/bin/env bash

export LD_LIBRARY_PATH=/pkg/momw/php/php/lib:/pkg/moip/mo11121/tools4prod/oracle12.1.0.4/lib
export MZ_HOME=/pkg/moip/mo11150/mzat/mz
export ORACLE_HOME=/pkg/moip/mo11121/tools4prod/oracle12.1.0.4
export PATH=/pkg/momw/php/php/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/VRTS/bin:/opt/VRTSvcs/bin:/pkg/moip/mo11121/tools4prod/oracle12.1.0.4/bin:/pkg/moip/mo11121/tools4prod/oracle12.1.0.4/bin:/pkg/moip/mo11150/mzat/mz/bin:/pkg/momw/java/java1.8_at/bin:/pkg/moip/mo11121/tools4prod/bin

python getIPsAndStructures.py mzadmin $1 mzrepat $2 pmzat1.appdb.ngIBMD.prod.mswo.de.tmo mzrepat