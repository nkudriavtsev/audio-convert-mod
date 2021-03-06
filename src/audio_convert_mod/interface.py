# -*- coding: utf-8 -*-
#  Copyright (C) 2007, 2008, 2009 Stewart Adam
#  This file is part of audio-convert-mod.

#  audio-convert-mod is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  audio-convert-mod is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with audio-convert-mod; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
Common classes for interfacing with Glade files
"""

from builtins import object
from gi.repository import Gtk, GObject
#import Gtk.glade
#Gtk.glade.bindtextdomain("audio-convert-mod")
# gtk
# |-- glade
#     |-- XML
#         |-- UserInterface     //Wraps a glade XML file
# Controller                    //Creates a UserInterface in 'ui'
# |-- audio-convert-mod                  //Starts program

class UserInterface(Gtk.Builder):
  """Base class for UIs loaded from glade."""
  def __init__(self, filename, rootWidget, domain):
    """
      Initialize a new instance.
      `filename' is the name of the .glade file containing the UI hierarchy.
      `rootname' is the name of the topmost widget to be loaded.
      `gladeDir' is the name of the directory, relative to the Python
      path, in which to search for `filename'
    """
    GObject.GObject.__init__(self)
    self.filename = filename
    self.set_translation_domain("audio-convert-mod")
    self.add_from_file(filename)
    self.root = self.get_object(rootWidget)

  # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

  def __getattr__(self, name):
    """Look up an as-yet undefined attribute, assuming it's a widget."""
    result = self.get_object(name)
    if result is None:
      raise AttributeError("Can't find widget %s in %s.\n" %
                 (repr(name), repr(self.filename)))

    # Cache the widget to speed up future lookups.  If multiple
    # widgets in a hierarchy have the same name, the lookup
    # behavior is non-deterministic just as for libglade.
    setattr(self, name, result)
    return result

class Controller(object):
  """ Base class for all controllers of glade-derived UIs. """
  def __init__(self, gladeFile, rootWidget):
    """ Initialize a new instance.
      `gladeFile' is the glade XML file. """
    # Create and ui object contains the widgets.
    self.ui = UserInterface(gladeFile, rootWidget, 'audio-convert-mod')
    self.ui.connect_signals(self._getAllMethods())

  def _getAllMethods(self):
    """ Get a dictionary of all methods in self's class hierarchy. """
    result = {}

    # Find all callable instance/class attributes.  This will miss
    # attributes which are "interpreted" via __getattr__.  By
    # convention such attributes should be listed in
    # self.__methods__.
    allAttrNames = list(self.__dict__.keys()) + self._getAllClassAttributes()
    for name in allAttrNames:
      value = getattr(self, name)
      if callable(value):
        result[name] = value
    return result

  # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

  def _getAllClassAttributes(self):
    """ Get a list of all attribute names in self's class hierarchy. """
    nameSet = {}
    for currClass in self._getAllClasses():
      nameSet.update(currClass.__dict__)
    result = list(nameSet.keys())
    return result

  # *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

  def _getAllClasses(self):
    """ Get all classes in self's heritage. """
    result = [self.__class__]
    i = 0
    while i < len(result):
      currClass = result[i]
      result.extend(list(currClass.__bases__))
      i = i + 1
    return result
