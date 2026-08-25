#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# Copyright (c) 2026 Gene C <arch@sapience.com>
#

project('py-cidr', ['c'],
  version: files('src/version.txt'),
  meson_version: '>=1.10.0',
  default_options: [
    'c_std=c23',
    'warning_level=3',
    'b_pie=true',
    'prefix=/usr',
    'mandir=share/man',
    ],
)

d_etc = get_option('sysconfdir')
d_lib = get_option('libdir')
d_bin = get_option('bindir')
d_man = get_option('mandir')
d_share = get_option('datadir')

py_mod = import('python')
py = py_mod.find_installation(pure: false)
src_root = meson.project_source_root()
py_dep = py.dependency(embed: true)

inc_dir = []
lib_sources = []

#
# top-level files
#

#
# Python submodules
#
subdir('src/py_cidr')

#
# Deps
#

#
# Executables
#
configure_file(
  input: 'src/prefixmap-print.py',
  output: 'prefixmap-printpy',
  copy: true,
  install_dir: d_bin,
  install_mode: 'rwxr-xr-x'
)

#
# Install
#
s_scripts = './scripts'
s_license = 'src/data/license'
s_changelog = 'src/data/changelog'
s_docs = 'src/data/docs'
manual = 'py-cidr.pdf'


#
# /usr/share/py-cidr/docs
#
install_data(
  [
    s_docs / manual,
    s_changelog / 'Changelog.rst',
  ],
  install_dir: d_share / 'py-cidr/docs'
)

install_subdir(
  [
    s_docs / 'html',
  ],
  install_dir: d_share / 'py-cidr/docs',
  strip_directory: false
)

#
# /usr/share/py-cidr/
#
install_data(
  [
    'README.rst',
    s_license / 'License-gpl-2.0.txt',
    s_license / 'License.rst',
    'packaging/PKGBUILD',
    'packaging/.nvchecker.toml',
    'packaging/Changelog',
  ],
  install_dir: d_share / 'py-cidr'
)

#
# /usr/share/licenses/py-cidr
#
install_data(
  [
    s_license / 'License-gpl-2.0.txt',
    s_license / 'License.rst',
  ],
  install_dir: d_share / 'licenses/py-cidr'
)

