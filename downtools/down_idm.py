__author__ = 'Wing'
import os, sys

count = 0


def add_to_idm(fname, path):
    global count
    with open(fname, 'r') as f:
        for i in f.readlines():
            count += 1
            cmd = 'IDMan /d "%s" /p "%s" /n /a ' % (i.strip(), path)
            print '[%i]%s' % (count, fname)
            os.system(cmd)


def loop_text_idm(p):
    root, dirs, files = os.walk(p).next()
    for name in files:
        if name.startswith('flickr_combine_'):
            add_to_idm(name, 'E:/Pixiv/flickr')
        elif name.startswith('pixiv_pt_combine_'):
            add_to_idm(name, 'E:/Pixiv/pt')
        elif name.startswith('pixiv_rnew_combine_'):
            add_to_idm(name, 'E:/Pixiv/r_new')
        elif name.startswith('pixiv_r_combine_'):
            add_to_idm(name, 'E:/Pixiv/r')
    os.system('IDMan;IDMan /s')


def run_aria(p, out, session):
    cmd = 'aria2c -i %s -j 20 -d %s --save-session=%s --referer=* --conditional-get=true' % (p, out, session)
    os.system(cmd)
    print cmd


def loop_text_aria(p):
    root, dirs, files = os.walk(p).next()
    for name in files:
        if name.startswith('flickr_combine_'):
            run_aria(name, 'E:/Pixiv/flickr', 'session_f.txt')
        elif name.startswith('pixiv_pt_combine_'):
            run_aria(name, 'E:/Pixiv/pt', 'session_p.txt')
        elif name.startswith('pixiv_r_new_combine_'):
            run_aria(name, 'E:/Pixiv/r_new', 'session_rn.txt')
        elif name.startswith('pixiv_r_combine_'):
            run_aria(name, 'E:/Pixiv/r', 'session_r.txt')


if __name__ == '__main__':
    if sys.argv[1] == 'aria':
        loop_text_aria('./')

