# -*- coding: utf-8 -*-
#    Copyright (C) 2007, 2008, 2009 Stewart Adam
#    This file is part of audio-convert-mod.

#    audio-convert-mod is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    audio-convert-mod is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with audio-convert-mod; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
audio-convert-mod package initialization
"""

#from future import standard_library
#standard_library.install_aliases()
from builtins import str
__author__ = "Stewart Adam <s.adam at diffingo.com>"
__status__ = "release"
__version__ = "4.0.0b"
__license__ = "GNU GPLv2+"

import os
import re
import sys
import unicodedata
from threading import Thread, Event

def CheckPerms(path):
  """ Checks for read and write permissions.
      Takes the path to check as an argument, returns
      True if permissions check out, False if not.
  """
  read = CheckPermsRead(path)
  write = CheckPermsWrite(path)
  if read == True and write == True:
      return True
  return False

def CheckPermsRead(path):
  """ Checks for read permissions.
      Takes the path to check as an argument, returns
      True if permissions check out, False if not.
  """
  if not os.path.exists(path):
    path = os.path.dirname(path)
  return os.access(path, os.R_OK)

def CheckPermsWrite(path):
  """ Checks for write permissions.
      Takes the path to check as an argument, returns
      True if permissions check out, False if not.
  """
  if not os.path.exists(path):
    path = os.path.dirname(path)
  return os.access(path, os.W_OK)

class FuncAsThread(Thread):
  """Run a function as a new thread."""
  def __init__(self, functorun, args):
    Thread.__init__(self)
    self.__args = args
    self.__functorun = functorun
    self.retval = None
    self.traceback = None
    self.exception = None

  def run(self):
    try:
      retval = self.__functorun(*self.__args)
      self.retval = retval
    except exceptions.SystemExit:
      # cancelled
      self.retval = -2
    except: # catch all other (non-request-for-cancel) exceptions
      # NOTE: Thread dies as soon as it gets the exception, so retval will be
      # None. Solution is to use "while thread.retval == None" rather than
      # "isAlive()" while checking for a return value.
      import traceback
      (etype, value, tb) = sys.exc_info()
      self.traceback = ''.join(traceback.format_exception(etype, value, tb))
      self.exception = etype(value)
      self.retval = -1
    return self.retval

def runFuncAsThread(functorun, *kargs):
  """Runs a function as a new thread"""
  thread = FuncAsThread(functorun, kargs)
  thread.start()
  return thread

def liststoreIntoArray(liststore):
  """ Turn a liststore into an array filled with it's rows and columns """
  def callback(model, path, iter, user_data):
    """ Just returns the contents of the row as a list """
    noColumns, allRows = user_data[0], user_data[1]
    currColumn = 0
    theRow = []
    # Append each value/column into the row list
    while currColumn < noColumns:
      theRow.append(model.get_value(iter, currColumn))
      currColumn = currColumn + 1
    # add this row to allRows
    allRows.append(theRow)
  # get number of columns, used in the loop in callback()
  noColumns = liststore.get_n_columns()
  allRows = []
  # run for each row - All rows get added to allRows
  liststore.foreach(callback, [noColumns, allRows])
  return allRows

def arrayIndex(array, text):
  """ A list's 'index' function for a arrays (multi-level lists)  """
  allMatches = []
  for i in array:
    try:
      # if found, let's get the key and index
      index = i.index(text)
      key = array.index(i)
      # if it doesn't exist, the above fails and we skip to except
      allMatches.append([key, index])
    except ValueError:
      # if not, just my mouth shut and keep executing
      pass
  return allMatches
  raise ValueError('array.index(text): text not in array')

def liststoreIndex(liststore, text):
  """ A list's 'index' function for a liststore  """
  # get the list
  liststoreArray = liststoreIntoArray(liststore)
  return liststoreArray, arrayIndex(liststoreArray, text)

def set_text_markup(label, text):
  """ set a Gtk.Label's text with markup """
  label.set_text(text)
  label.set_use_markup(True)

def remove_diacritics(string):
  """ Removed diacritics from the string """
  reCombining = re.compile(u'[\u0300-\u036f\u1dc0-\u1dff\u20d0-\u20ff\ufe20-\ufe2f]', re.U)
  return reCombining.sub('', unicodedata.normalize('NFD', str(string, sys.stdin.encoding)) )
