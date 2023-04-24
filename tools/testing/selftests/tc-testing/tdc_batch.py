#!/usr/bin/python3

"""
tdc_batch.py - a script to generate TC batch file

Copyright (C) 2017 Chris Mi <chrism@mellanox.com>
"""


import argparse

parser = argparse.ArgumentParser(description='TC batch file generator')
parser.add_argument("device", help="device name")
parser.add_argument("file", help="batch file name")
parser.add_argument("-n", "--number", type=int,
                    help="how many lines in batch file")
parser.add_argument("-o", "--skip_sw",
                    help="skip_sw (offload), by default skip_hw",
                    action="store_true")
parser.add_argument("-s", "--share_action",
                    help="all filters share the same action",
                    action="store_true")
parser.add_argument("-p", "--prio",
                    help="all filters have different prio",
                    action="store_true")
args = parser.parse_args()

device = args.device
file = open(args.file, 'w')

number = args.number if args.number else 1
skip = "skip_sw" if args.skip_sw else "skip_hw"
share_action = "index 1" if args.share_action else ""
prio = "prio 1"
if args.prio:
    prio = ""
    number = min(number, 0x4000)
index = 0
for i in range(0x100):
    for j in range(0x100):
        for k in range(0x100):
            mac = ("%02x:%02x:%02x" % (i, j, k))
            src_mac = f"e4:11:00:{mac}"
            dst_mac = f"e4:12:00:{mac}"
            cmd = f"filter add dev {device} {prio} protocol ip parent ffff: flower {skip} src_mac {src_mac} dst_mac {dst_mac} action drop {share_action}"
            file.write("%s\n" % cmd)
            index += 1
            if index >= number:
                file.close()
                exit(0)
