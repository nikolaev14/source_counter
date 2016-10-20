#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import argparse

import lang_ext


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',
                        default='./',
                        type=str,
                        help='Path to start dir')

    return parser


lang_ext_base = lang_ext.lang_ext
files_path = []
files_per_lang = {}
lang_files = {}
lang_files_space = {}
final = {}


def path_dir_files(path, fp):
    for path, dirs, files in os.walk(path):
        for file in files:
            fp.append(path + "/" + file)


def fill_files_per_lang(leb, fp, lf):
    # leb = lang_ext_base
    # fp = files_path
    # lf = lang_files
    for lang in leb:
        lf[lang] = []
        x = leb[lang]
        for f in fp:
            if f.endswith(x):
                lf[lang].append(f)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    topdir = namespace.path
    path_dir_files(topdir, files_path)
    fill_files_per_lang(lang_ext_base, files_path, lang_files)

    for lang in lang_files:
        if len(lang_files[lang]) > 0:
            for file in lang_files[lang]:
                if lang not in lang_files_space:
                    lang_files_space[lang] = 0
                else:
                    lang_files_space[lang] += os.path.getsize(file)

    for l in lang_files_space:
        if lang_files_space[l] > 0:
            final[l] = [round(lang_files_space[l] / (1024 * 1024.00), 3),
                        len(lang_files[l])]

    final = sorted(final.items(), key=lambda (k, v): v[1], reverse=True)
    for i in final:
        # print i[0] + ":\t", "|\t", i[1][1], "file`s\t|\t", i[1][0], "Mb"
        print i[0] + ":\t", "|\t", i[1][1], "\t|\t", i[1][0]
