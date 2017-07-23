# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-23 下午1:31
# @File    : create_child_class_test.py

class AddrBookEntry(object):
    def __init__(self, nm, ph):
        self.name = nm
        self.phone = ph
        print('created')
    def update_phone(self):
        pass

class EmplAddrBookEntry(AddrBookEntry):
    def __init__(self, nm, ph, id, em):
        AddrBookEntry.__init__(self, nm, ph)
        self.empid = id
        self.email = em

    def update_email(self):
        pass

