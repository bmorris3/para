#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
pbs.py
------

Generates a ``PBS`` script and launches a ``qsub`` job on a cluster.

'''

from __future__ import division, print_function, absolute_import, unicode_literals
import time
import os
import subprocess

__all__ = ['qsub']

PBS_MPI = \
"""
#!/bin/sh
%(NAME)s
#PBS -l nodes=%(NODES)d:ppn=%(PPN)d,feature=%(PPN)dcore,mem=%(MEM)dgb,walltime=%(WALLTIME)s
%(STDOUT)s
%(STDERR)s
%(EMAIL)s
%(CMDS)s
cd %(PATH)s
mpiexec -np $PBS_NP python %(SCRIPT)s%(ARGS)s
"""

def qsub(script, path = None, nodes = 2, ppn = 12, mem = 40, 
         hours = 1., stdout = None, stderr = None, email = None, 
         args = None, logfile = None, cmds = None, name = None):
  '''
  
  '''
  
  if path is None:
    path = os.getcwd()
  if name is not None:
    name = "#PBS -n %s" % name
  else:
    name = ''
  walltime = time.strftime('%H:%M:%S', time.gmtime(hours * 3600.))
  if stdout is not None:
    stdout = "#PBS -o %s" % stdout
  else:
    stdout = ''
  if stderr is not None:
    stderr = "#PBS -e %s" % stderr
  else:
    stderr = ''
  if email is not None:
    email = "#PBS -M %s\n#PBS -m abe" % email
  else:
    email = ''
  if args is not None:
    args = ' ' + ' '.join(args)
  else:
    args = ''
  if logfile is not None:
    args = args + ' &> ' + logfile
  if cmds is None:
    cmds = ''
  
  with open('script.pbs', 'w') as f:
    contents = PBS_MPI % {'NODES': nodes, 'PPN': ppn, 'MEM': mem, 'WALLTIME': walltime,
                          'STDOUT': stdout, 'STDERR': stderr, 'EMAIL': email, 
                          'SCRIPT': script, 'ARGS': args, 'PATH': path,
                          'CMDS': cmds, 'NAME': name}
    print(contents, file = f)
  
  try:
    subprocess.call(['qsub', 'script.pbs'])
  except FileNotFoundError:
    raise Exception("Unable to launch the script using qsub.")