# Copyright (C) 2022 National Center for Atmospheric Research and National Oceanic and Atmospheric Administration
# SPDX-License-Identifier: Apache-2.0
#
import os
import sys
import argparse
import logging
import yaml
from glob import glob

parser = argparse.ArgumentParser()
parser.add_argument('--control', type=str,
    default='control.yaml',
    help='yaml control file')
parser.add_argument('--logfile', type=str,
    default=sys.stdout,
    help='log file (default: stdout)')
parser.add_argument('--outdir', type=str,
    default=None,
    help='output directory')
parser.add_argument('--debug', action='store_true',
    help='set logging level to debug')
args = parser.parse_args()

"""
Setup logging
"""
logging_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(stream=args.logfile, level=logging_level)

"""
Read YAML control
"""
with open(args.control, 'r') as f:
    control = yaml.safe_load(f)

logging.debug(control)

for model in control['model']:
    logging.info('processing:' + model)

    var_str = '-v '

    if 'required_vars' in control['model'][model]:
        for var in control['model'][model]['required_vars']:
            var_str += var + ','

    """
    for dataset in control['model'][model]['mapping']:
        for var in control['model'][model]['mapping'][dataset]:
            var_str += var + ','
    """
    for var in control['model'][model]['variables']:
        var_str += var + ','

    var_str = var_str.strip(',')
    logging.info(var_str)

    file_str = os.path.expandvars(control['model'][model]['files'])

    files = sorted(glob(file_str))

    for file_in in files:
        file_subdirs = list(os.path.split(file_in))
        file_subdirs[-1] = 'subset_' + file_subdirs[-1]
        if args.outdir is not None:
            file_out = os.path.join(args.outdir, file_subdirs[-1])
        else:
            file_out = os.path.join(file_subdirs)
        command = f'ncks -O {var_str} {file_in} {file_out}'
        logging.info(command)
        os.system(command)

