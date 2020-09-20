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
prefs.defaults['hello_world_msg'] = 'Hello, World!'
prefs.defaults['query_max_res'] = 10
prefs.defaults['query_to_comment'] = True
prefs.defaults['query_extra_by_name'] = False


class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.l = QFormLayout(self)
        self.setLayout(self.l)

        # self.label = QLabel('Hello world &message:')
        self.msg = QLineEdit(self)
        self.msg.setText(prefs['hello_world_msg'])
        self.l.addRow("hello world message:",self.msg)
        # self.label.setBuddy(self.msg)

        # self.max_res_label = QLabel('Max results:')
        self.max_res = QLineEdit(self)
        self.max_res.setText(str(prefs['query_max_res']))
        self.max_res.setValidator(QIntValidator(1, 99, self))
        self.l.addRow(_('Maximum results:'), self.max_res)
        # self.label.setBuddy(self.max_res_label)
        self.write_comments = QCheckBox(_('Write additional info in comments'), self)
        self.write_comments.setChecked(prefs['query_to_comment'])
        self.l.addRow(self.write_comments)

        self.extraq = QCheckBox(_('Search already identified anew'), self)
        self.write_comments.setChecked(prefs['query_extra_by_name'])
        self.l.addRow(self.extraq)

    def save_settings(self):
        prefs['hello_world_msg'] = self.msg.text()
        prefs['query_max_res'] = int(self.max_res.text())
        # print("hi")
        # print(self.write_comments.checkState())
        # print(self.write_comments.checkState() == Qt.Checked)
        prefs['query_to_comment'] = self.write_comments.checkState() == Qt.Checked
        prefs['query_extra_by_name'] = self.extraq.checkState() == Qt.Checked
