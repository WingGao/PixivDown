REM :: flickr
REM type flickr_combine_*.txt > fc.txt
REM aria2c -i fc.txt -j 10 -d flickr --save-session=s_fc.txt
REM :: pixiv normal
REM type pixiv_pt_combine_*.txt > ptc.txt
REM aria2c -i ptc.txt -j 10 -d pt --save-session=s_ptc.txt --referer=*
REM :: pixiv 18
REM type pixiv_r_combine_*.txt > prc.txt
REM aria2c -i prc.txt -j 10 -d r --save-session=s_prc.txt --referer=*
REM :: pixiv 18 new 
REM type pixiv_r_new_combine_*.txt > prnc.txt
REM aria2c -i prnc.txt -j 10 -d r_new --save-session=s_prnc.txt --referer=*

down_idm.py aria