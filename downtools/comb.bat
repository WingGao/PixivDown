@echo off
pause
echo Combine?
pause
type flickr_export_*.txt > flickr_comb.txt
type pixiv_pt_export_*.txt > pixiv_pt_comb.txt
type pixiv_r_export_*.txt > pixiv_r_comb.txt
echo Remove?
pause
del flickr_export_*.txt
del pixiv_pt_export_*.txt
del pixiv_r_export_*.txt