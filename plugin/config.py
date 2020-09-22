#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import absolute_import, division, print_function, unicode_literals

__license__   = 'GPL v3'
__copyright__ = '2011, Kovid Goyal <kovid@kovidgoyal.net>'
__docformat__ = 'restructuredtext en'

from PyQt5.Qt import QWidget, QHBoxLayout, QLabel, QLineEdit, QIntValidator, QFormLayout, QCheckBox, Qt

from calibre.utils.config import JSONConfig

# This is where all preferences for this plugin will be stored
# Remember that this name (i.e. plugins/doi_meta) is also
# in a global namespace, so make it as unique as possible.
# You should always prefix your config file name with plugins/,
# so as to ensure you dont accidentally clobber a calibre config file
prefs = JSONConfig('plugins/doi_meta')

# Set defaults
# prefs.defaults['query_max_res'] = 10
prefs.defaults['abstract_to_comment'] = True
prefs.defaults['query_to_comment'] = True
prefs.defaults['query_extra_by_name'] = False
prefs.defaults['add_tags'] = False

prefs.defaults['prefer_short_title'] = False
prefs.defaults['prefer_short_journal'] = False

class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.l = QFormLayout(self)
        self.setLayout(self.l)
        self.form_elements = {}

        self.put_element(
            'prefer_short_title',
            QCheckBox(_('Prefer short title if available'), self)
        )
        self.put_element(
            'prefer_short_journal',
            QCheckBox(_('Prefer short journal name if available'), self)
        )

        self.put_element(
            'abstract_to_comment',
            QCheckBox(_('Put abstract in comment'), self)
        )
        self.put_element(
            'query_to_comment',
            QCheckBox(_('Write additional info in comments'), self)
        )
        self.put_element(
            'query_extra_by_name',
            QCheckBox(_('If object has DOI also search by title'), self)
        )
        self.put_element(
            'add_tags',
            QCheckBox(_('Store Subjects as tags'), self)
        )
        self.init_editors()


    def put_element(self, name, widget, title=None):
        if not self.form_elements.has_key(name):
            self.form_elements[name] = widget
            if title:
                self.l.addRow(title,widget)
            else:
                self.l.addRow(widget)
        else:
            raise Exception("Duplicate preference: %s", name)

    def init_editors(self):
        for key,obj in self.form_elements.items():
            if isinstance(obj, QCheckBox):
                obj.setChecked(prefs[key])
            elif isinstance(obj, QLineEdit):
                obj.setText(str(prefs[key]))
            else:
                raise Exception("unimplemented pref for: %s", obj)

    def save_settings(self):
        for key,obj in self.form_elements.items():
            if isinstance(obj, QCheckBox):
                print("Checkbox %s" % key)
                print("Value %s" % obj.checkState)
                prefs[key] = obj.checkState() == Qt.Checked
            elif isinstance(obj, QLineEdit):
                prefs[key] = obj.text()
            else:
                raise Exception("unimplemented pref for: %s", obj)

        # # self.max_res_label = QLabel('Max results:')
        # self.max_res = QLineEdit(self)
        # self.max_res.setText(str(prefs['query_max_res']))
        # self.max_res.setValidator(QIntValidator(1, 99, self))
