t=`date +"%Y-%m-%d"`
tar -cf combine_$t.tar *_combine_* --remove-files
mpack -s "combine_$t" combine_$t.tar 459171748@qq.com
