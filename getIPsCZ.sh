#!/usr/bin/env bash

export LD_LIBRARY_PATH=/pkg/momw/php/php/lib:/pkg/moip/mo11121/tools4prod/oracle12.1.0.4/lib
export MZ_HOME=/pkg/moip/mo11160/mzcz/mz
export ORACLE_HOME=/pkg/moip/mo11121/tools4prod/oracle12.1.0.4
export PATH=pkg/momw/php/php/bin:/pkg/momw/php/php/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/opt/VRTS/bin:/opt/VRTSvcs/bin:/pkg/moip/mo11121/tools4prod/oracle12.1.0.4/bin:/pkg/moip/mo11160/mzcz/cust/bin:/pkg/moip/mo11160/mzcz/cust/bin/asn:/pkg/moip/mo11160/mzcz/mz/bin:/pkg/momw/java/java1.8_cz/bin:/usr/local/sbin:/usr/sbin:/sbin:/pkg/moip/mo11121/tools4prod/oracle12.1.0.4/bin:/pkg/moip/mo11160/mzcz/cust/bin:/pkg/moip/mo11160/mzcz/cust/bin/asn:/pkg/moip/mo11160/mzcz/mz/bin:/pkg/momw/java/java1.8_cz/bin

python getIPsAndStructures.py mzadmin $1 mzrepcz $2 pmzcz1.appdb.ngIBMD.prod.mswo.de.tmo mzrepcz