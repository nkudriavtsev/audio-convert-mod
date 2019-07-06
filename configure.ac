#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([audio-convert-mod], [4.0.0])
AM_INIT_AUTOMAKE([dist-bzip2 no-dist-gzip])
AC_CONFIG_SRCDIR(src/audio_convert_mod/__init__.py.in)

# Checks for programs.
# Search for Python >= 3.6
AM_PATH_PYTHON([3.6])

# Setup gettext translation
ALL_LINGUAS="zh_CN"
GETTEXT_PACKAGE=audio-convert-mod
AC_SUBST(GETTEXT_PACKAGE)
# Use intltool
AC_PROG_INTLTOOL

AC_CONFIG_FILES([Makefile
                 bin/Makefile
                 bin/audio-convert-mod
                 src/Makefile
                 src/audio_convert_mod/Makefile
                 src/audio_convert_mod/__init__.py
                 po/Makefile.in
                 ])

# ...Ready, set, go!
AC_OUTPUT
