__author__ = 'Wing'
import os
import json
import sys
import re
import argparse

try:
    from win32api import CopyFile as copyfile
except:
    from shutil import copyfile

__version__ = '1.0'


class JobType():
    COPY = 'copy'
    MOVE = 'move'
    DELETE = 'delete'


class Job():
    def __init__(self, job):
        self.dir_f = os.path.abspath(job['dir_from'])
        self.dir_t = os.path.abspath(job['dir_to'])
        self.job_type = job['action']
        self.ignores = job['ignores']
        self.is_overwrite = False

        if 'option' in job:
            self.is_overwrite = 'overwrite' in job['option']

        if 'limit' in job:
            self.limit = job['limit']
        else:
            self.limit = 0

    def __move_file(self, ff, ft):
        if not os.path.exists(ft) or self.is_overwrite:
            os.rename(ff, ft)
        else:
            os.remove(ff)

    def __copy_file(self, ff, ft):
        if not os.path.exists(ft) or self.is_overwrite:
            copyfile(ff, ft)

    def __delete_file(self, ff):
        #will raise error 32
        os.remove(ff)

    def __get_file_toname(self, f):
        return f.replace(self.dir_f, self.dir_t)

    def __is_ignore(self, f):
        for i in self.ignores:
            if re.search(i, f):
                return True
        return False


    def do(self):
        print '[JOB-START] %s %s %s' % (self.dir_f, self.job_type, self.dir_t)
        files_f = get_files(self.dir_f)
        ignore_num = 0
        for i, v in enumerate(files_f):
            if 0 < self.limit:
                if self.limit <= i + ignore_num:
                    break
                print_progress(i + 1 - ignore_num, self.limit, v)
            else:
                print_progress(i + 1, len(files_f), v)
            if not self.__is_ignore(v):
                ft = self.__get_file_toname(v)
                check_file_dir(ft)
                try:
                    if self.job_type == JobType.COPY:
                        self.__copy_file(v, ft)
                    elif self.job_type == JobType.MOVE:
                        self.__move_file(v, ft)
                    elif self.job_type == JobType.DELETE:
                        self.__delete_file(v)
                except WindowsError:
                    print '[ERROR]'
            else:
                print '[IGNORE]'
                ignore_num += 1
        print '\n[JOB-FINISH]'


def load_conf(fp):
    with open(fp, 'r') as f:
        return json.load(f)


def get_files(path):
    fl = []
    for root, dirs, files in os.walk(path):
        for i in files:
            fp = os.path.join(root, i)
            fl.append(fp)
    return fl


def check_file_dir(fpath):
    fdir = os.path.dirname(fpath)
    if not os.path.exists(fdir):
        os.mkdir(fdir)


def print_progress(i, all, v):
    print '\r[%.2f%%] %s\t\t' % (i * 100.0 / all, v),


if __name__ == '__main__':
    sc = 'Python move file by Wing %s' % __version__
    print sc
    parser = argparse.ArgumentParser(description=sc)
    parser.add_argument('-act', metavar='action', help='m=move')
    parser.add_argument('-f', metavar='from_dir')
    parser.add_argument('-t', metavar='to_dir')
    parser.add_argument('--limit', metavar='limit file numbers', type=int, default=0)
    parser.add_argument('--conf', metavar='config file', help='load action from a file')
    args = parser.parse_args()
    if args.conf is not None:
        conf = load_conf(os.path.abspath(args.conf))
        for i in conf:
            job = Job(i)
            job.do()
    else:
        c = {'action': args.act, 'dir_from': args.f, 'dir_to': args.t, 'limit': args.limit,
             'ignores': ['\\\\\.']}
        print c
        job = Job(c)
        job.do()
