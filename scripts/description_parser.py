import os

path = os.getcwd() + "/"

white_list_names = ["pl_wl1","DB_wl","plaforms_wl","tools_wl",
                    "web_Frame_wl","env_wl","workflow_wl","test_wl", "vis_wl"]

class descript:
    def __init__(self, _ID):
        self.ID = _ID
        self.langs = ""
        self.dbs = ""
        self.plat = ""
        self.tools = ""
        self.web = ""
        self.workflow = ""
        self.test = ""
        self.vis = ""
        self.modified = False

    def add_lang(self, _lang):
        self.lang += _lang + " "
        self.modified = True

    def add_dbs(self, _db):
        self.dbs += _db + " "
        self.modified = True

    def add_plat(self, _plat):
        self.plat += _plat + " "
        self.modified = True

    def add_tools(self, _tool):
        self.tools += _tool + " "
        self.modified = True

    def add_web(self, _web):
        self.web += _web + " "
        self.modified = True

    def add_workflow(self, _wf):
        self.workflow += _wf + " "
        self.modified = True

    def add_test(self, _test):
        self.test += _test + " "
        self.modified = True

    def add_vis(self, _vis):
        self.vis+= _vis + " "
        self.modified = True