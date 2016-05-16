#!/usr/bin/env python3

import argparse
import os
import site
import subprocess


def error(msg):
  print('ERROR: {0}'.format(msg))
  exit(-1)


def doit(cmd, failsafe=False):
  print('EXEC: {0}'.format(cmd))
  try:
    subprocess.check_call(cmd, shell=True)
    return True
  except:
    if failsafe:
      return False
    else:
      error(cmd)


def nic_cc(loc, url, commit, cpus):
  print('CC REPO: {0}'.format(url))
  doit('git clone {0} {1}'.format(url, loc))
  if commit:
    doit('cd {0} && git checkout {1}'.format(loc, commit))
  doit('cd {0} && sed -i \'s@$(HOME)/.makeccpp@../makeccpp@g\' Makefile'
       .format(loc))
  doit('cd {0} && sed -i \'s@:= ../../@:= ../@g\' Makefile'
       .format(loc))
  doit('cd {0} && sed -i \'s@-march=native@@g\' Makefile'
       .format(loc))
  doit('cd {0} && make -j {1} && make check'.format(loc, cpus))


def nic_py(loc, url, commit, cpus):
  print('PY REPO: {0}'.format(url))
  doit('git clone {0} {1}'.format(url, loc))
  if commit:
    doit('cd {0} && git checkout {1}'.format(loc, commit))
  doit('cd {0} && python3 setup.py install --user'.format(loc))


def pip_py(package, user=True):
  print('PY PKG: {0}'.format(package))
  if not doit('python3 -c "import {0}"'.format(package), True):
    user = '--user' if user else ''
    doit('pip3 install {0} {1}'.format(package, user))


def check(thing):
  if os.path.isfile(os.path.join(thing, '.installed')):
    return False
  else:
    doit('rm -rf {0}'.format(thing))
    return True


def complete(thing):
  doit('touch {0}'.format(os.path.join(thing, '.installed')), True)


def main(args):
  loc = args.location

  if not os.path.isdir(loc):
    try:
      os.mkdir(loc)
    except Exception as ex:
      error(ex)
  assert os.path.isdir(loc)

  cpus = args.cpus
  if cpus == 0:
    cpus = 1

  print('installing Homework 3 environment to {0}'.format(loc))

  userbase = site.USER_BASE
  userbin = os.path.join(userbase, 'bin')
  if userbin not in os.environ['PATH'].split(':'):
    error(('\nThis environment requires some Python packages installed\n'
           'locally as \'user\' packages. You must add \'{0}\'\n'
           'to your PATH environment variable. Add the following to your\n'
           'startup script (e.g., ~/.bashrc) and try again:\n'
           '\n'
           'For bash:\n'
           '  PATH="{0}:$PATH"\n'
           'For csh/tcsh:\n'
           '  setenv PATH {0}\:$PATH\n'
           '\n').format(userbin))

  if not doit('python3 -c "import matplotlib"', True):
    print(('***************\n'
           'This system requires python3-matplotlib to be installed\n'
           'On Ubuntu you can run:\n'
           '   sudo apt-get install python3-matplotlib'))
    error('dependency failure')

  if not doit('python3 -c "import numpy"', True):
    print(('***************\n'
           'This system requires python3-numpy to be installed\n'
           'On Ubuntu you can run:\n'
           '   sudo apt-get install python3-numpy'))
    error('dependency failure')

  if not doit('dpkg -l zlib1g-dev', True):
    print(('***************\n'
           'This system requires zlib1g-dev to be installed\n'
           'On Ubuntu you can run:\n'
           '   sudo apt-get install zlib1g-dev'))
    error('dependency failure')

  makeccpp = os.path.join(loc, 'makeccpp')
  if check(makeccpp):
    try:
      os.mkdir(makeccpp)
    except Exception as ex:
      error(ex)
    assert os.path.isdir(makeccpp)

    doit(('wget https://raw.githubusercontent.com/nicmcd/make-c-cpp/master/'
          'auto_bin.mk -O {0}/auto_bin.mk').format(makeccpp))
    doit(('wget https://raw.githubusercontent.com/nicmcd/make-c-cpp/master/'
          'auto_lib.mk -O {0}/auto_lib.mk').format(makeccpp))
    complete(makeccpp)

  gtest = os.path.join(makeccpp, 'gtest')
  if check(gtest):
    doit('git clone https://github.com/nicmcd/gtest.git {0}'.format(gtest))
    doit('cd {0} && make -j {1} gtest_main.a'.format(
      os.path.join(gtest, 'make'), cpus))
    complete(gtest)

  cpplint = os.path.join(makeccpp, 'cpplint')
  if check(cpplint):
    doit('git clone https://github.com/nicmcd/cpplint.git {0}'
         .format(cpplint))
    complete(cpplint)

  libprim = os.path.join(loc, 'libprim')
  if check(libprim):
    nic_cc(libprim, 'https://github.com/nicmcd/libprim.git', None, cpus)
    complete(libprim)

  librnd = os.path.join(loc, 'librnd')
  if check(librnd):
    nic_cc(librnd, 'https://github.com/nicmcd/librnd.git', None, cpus)
    complete(librnd)

  libmut = os.path.join(loc, 'libmut')
  if check(libmut):
    nic_cc(libmut, 'https://github.com/nicmcd/libmut.git', None, cpus)
    complete(libmut)

  libbits = os.path.join(loc, 'libbits')
  if check(libbits):
    nic_cc(libbits, 'https://github.com/nicmcd/libbits.git', None, cpus)
    complete(libbits)

  libjson = os.path.join(loc, 'libjson')
  if check(libjson):
    nic_cc(libjson, 'https://github.com/nicmcd/libjson.git', None, cpus)
    complete(libjson)

  libsettings = os.path.join(loc, 'libsettings')
  if check(libsettings):
    nic_cc(libsettings, 'https://github.com/nicmcd/libsettings.git', None, cpus)
    complete(libsettings)

  libstrop = os.path.join(loc, 'libstrop')
  if check(libstrop):
    nic_cc(libstrop, 'https://github.com/nicmcd/libstrop.git', None, cpus)
    complete(libstrop)

  taskrun = os.path.join(loc, 'taskrun')
  if check(taskrun):
    doit('rm -rf {0}/lib/python3*/site-packages/taskrun*'.format(userbase))
    doit('rm -rf {0}/lib/python3*/site-packages/psutil*'.format(userbase))
    doit('rm -rf {0}/lib/python3*/site-packages/termcolor*'.format(userbase))
    nic_py(taskrun, 'https://github.com/nicmcd/taskrun.git', None, cpus)
    doit('python3 -c "import taskrun"')
    complete(taskrun)

  supersim = os.path.join(loc, 'supersim')
  if check(supersim):
    nic_cc(supersim, 'https://github.com/hpelabs/supersim.git', 'dev', cpus)
    complete(supersim)

  sslatency = os.path.join(loc, 'sslatency')
  if check(sslatency):
    nic_cc(sslatency, 'https://github.com/nicmcd/sslatency.git', None, cpus)
    complete(sslatency)

  percentile = os.path.join(loc, 'percentile')
  if check(percentile):
    doit('rm -rf {0}/lib/python3*/site-packages/percentile*'.format(userbase))
    nic_py(percentile, 'https://github.com/nicmcd/percentile.git', None, cpus)
    doit('python3 -c "import percentile"')
    complete(percentile)

  ssplot = os.path.join(loc, 'ssplot')
  if check(ssplot):
    doit('rm -rf {0}/bin/sslqp'.format(userbase))
    doit('rm -rf {0}/bin/ssllp'.format(userbase))
    doit('rm -rf {0}/lib/python3*/site-packages/ssplot*'.format(userbase))
    nic_py(ssplot, 'https://github.com/nicmcd/ssplot.git', None, cpus)
    doit('python3 -c "import ssplot"')
    doit('sslqp -h')
    doit('ssllp -h')
    complete(ssplot)

  print(('\n\n'
         '*********************************************************\n'
         '****** Homework 3 environment built successfully! *******\n'
         '*********************************************************\n'
         '\n'))


if __name__ == '__main__':
  ap = argparse.ArgumentParser()
  ap.add_argument('location',
                  help='the location of installation')
  ap.add_argument('-c', '--cpus', type=int, default=os.cpu_count(),
                  help='make -j option value (parallel make)')
  args = ap.parse_args()
  exit(main(args))
