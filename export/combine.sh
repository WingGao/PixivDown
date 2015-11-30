t=`date +"%Y-%m-%d"`
echo "start $t"
cat flickr_export_* >> flickr_combine_$t.txt
cat pixiv_pt_export_* >> pixiv_pt_combine_$t.txt
cat pixiv_r_export_* >> pixiv_r_combine_$t.txt
cat pixiv_r_new_export_* >> pixiv_r_new_combine_$t.txt
echo "combine finish"
rm *_export_*
echo "remove finish"
