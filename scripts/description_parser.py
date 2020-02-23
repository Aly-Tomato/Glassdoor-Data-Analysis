import os,re, csv
from bs4 import BeautifulSoup
import langdetect

path = os.getcwd() + "/"

white_list_names = ["pl_wl1","DB_wl","plaforms_wl","tools_wl",
                    "web_Frame_wl","env_wl","workflow_wl","test_wl", "vis_wl"]

desc_file_path = "/Users/chrism/Data_sci/desc.csv"

class descript:
    def __init__(self, _ID, _wl_list):
        self.ID = _ID

        self.lists_cats = {}
        for list_name in _wl_list:
            temp = {list_name: {}}
            self.lists_cats.update(temp)

        self.modified = False

    def add_term(self,wlist_name, word):
        temp = self.lists_cats[wlist_name]
        if temp.get(word) == None:
            temp[word] = 1
        self.lists_cats[wlist_name] = temp
        self.modified = True

    def get_id(self):
        return self.ID

    def print_data(self):
        if self.modified:
            outstring = self.ID
            for key,values in self.lists_cats.items():
                outstring += ',"'
                for words, count in values.items():
                    outstring += words + " "

 

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


def digest(desc,wl_names,wlists, global_counts, job_entry):
    desc = desc.replace('\n',' ')
    desc_list = desc.split(' ')
    for word in desc_list:
        cur_wl = check_lists(word,wl_names,wlists)
        if cur_wl:
            job_entry.add_term(cur_wl,word)
            temp = global_counts[cur_wl]
            if temp.get(word) == None:
                temp[word] = 1
            else:
                temp[word] += 1
            global_counts[cur_wl] = temp
            


def check_lists(word,wl_names, white_lists):
    for i in range(0,len(wl_names)):
        if word in white_lists[i]:
            return wl_names[i]

def print_global_dict(gd):
    #print(gd)
    for key, values in gd.items():
        if gd[key]:
            #print(key)
            for words, counts in values.items():
                print(words + "," + str(counts))


def main(w_l_names,desc_path ):
    entry_list = []
    global_counts = make_global_count_dict(w_l_names)
    white_lists = load_white_list(w_l_names)
    count = 0
    with open(desc_path, 'r') as csvfile:
        entries = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in entries:
            jobid = row["gaTrackerData.jobId"]
            cur_job = descript(jobid,w_l_names)
            desc_entry = row["job.description"]
            if langdetect.detect(desc_entry) == "en":
                soup = BeautifulSoup(desc_entry, "lxml")
                experience = soup.find_all(string=re.compile("experience"))
                first_pass = re.sub("[->,\"%#/&$().?'!:*\t\[\]]", ' ', soup.get_text(separator=' '))
                digest(desc_entry,w_l_names,white_lists,global_counts,cur_job)
                count += 1
            if count % 5 == 0:
                break

    header = "jobid,"
    for name in white_list_names:
        header += name + ","
    print(header)

    print_global_dict(global_counts)



main(white_list_names,desc_file_path)

