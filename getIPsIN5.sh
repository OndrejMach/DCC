#!/usr/bin/env bash

export LD_LIBRARY_PATH=/pkg/moip/data_user/tools/lib:/pkg/moip/data_user/tools/local/mysql/lib:/pkg/moip/data_user/tools/local/lib:/pkg/moip/data_user/tools/local/ruby-2.2.4/lib:/usr/local/lib:/pkg/moip/mo10754/oracle/product/12.1.0.2/lib::/pkg/moip/data_user/tools/dec//lib
export MZ_HOME=/pkg/moip/app1_mzin/mzIN5/mz
export ORACLE_HOME=/pkg/moip/mo10754/oracle/product/12.1.0.2
export PATH=/pkg/moip/app1_mzin/mzIN5/app/tools/bin:/pkg/moip/data_user/tools/dec//bin:/pkg/moip/data_user/tools/bin:/pkg/moip/app1_mzin/mzIN5/ngrtt/bin:/pkg/moip/mo11115_common/MSS_TS/tools/bin:/pkg/moip/mo11115_common/AutomaticTests/bin:/pkg/moip/mo11115_common/tmd_tools:/pkg/moip/app1_mzin/mzIN5/bin:/pkg/moip/app1_mzin/mzIN5/mz/bin:/pkg/moip/data_user/tools/local/bin:/pkg/moip/data_user/tools/local/mysql/bin:/pkg/moip/data_user/tools/local/httpd/bin:/pkg/moip/data_user/tools/local/ruby-2.2.4/bin:/pkg/moip/mo10754/oracle/product/12.1.0.2/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/pkg/momw/java/jdk1.8.0_66_64bit/bin:/pkg/momw/java/jdk1.8.0_66_64bit/jre/bin:/usr/kerberos/bin:/usr/local/bin:/bin:/usr/bin:/pkg/moip/app1_mzin/mzIN5/app/bin


python getIPsAndStructures.py mzadmin $1 mzrepIN5 $2 tMZTUA1 mzrepIN5