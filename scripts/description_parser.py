import os,re, csv
from bs4 import BeautifulSoup
import langdetect

path = os.getcwd() + "/"

white_list_names = ["pl_wl1","DB_wl","plaforms_wl","tools_wl",
                    "web_Frame_wl","env_wl","workflow_wl","test_wl", "vis_wl"]

desc_file_path = "/Users/chrism/Data_sci/desc.csv"

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
        self.langs += _lang + " "
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



def load_white_list(wl_names):
    list_of_wl = []
    for name in wl_names:
        file_name = os.getcwd() + "/white_lists/" + name + ".txt"
        wl_set = set()
        wl_file = open(file_name, 'r')
        for line in wl_file:
            line = line.strip()
            #line = line.lower()
            wl_set.add(str(line))
        list_of_wl.append(wl_set)
    return list_of_wl


def make_global_count_dict(wl_names):
    global_dict = {}
    for wl_name in wl_names:
        temp = {wl_name: {}}
        global_dict.update(temp)
    return global_dict


def main(w_l_names,desc_path ):
    entry_list = []
    global_counts = make_global_count_dict(w_l_names)
    white_lists = load_white_list(w_l_names)
    with open(desc_path, 'r') as csvfile:
        entries = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in entries:
            jobid = row["gaTrackerData.jobId"]
            cur_job = descript(jobid)
            desc_entry = row["job.description"]
            if langdetect.detect(desc_entry) == "en":
                soup = BeautifulSoup(desc_entry, "lxml")
                experience = soup.find_all(string=re.compile("experience"))
                first_pass = re.sub("[->,\"%#/&$().?'!:*\t\[\]]", ' ', soup.get_text(separator=' '))
                



main(white_list_names,desc_file_path)

