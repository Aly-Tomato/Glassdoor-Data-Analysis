import os,re, csv
from bs4 import BeautifulSoup
import langdetect

path = os.getcwd() + "/"

white_list_names = ["pl_wl1","DB_wl","plaforms_wl","tools_wl",
                    "web_Frame_wl","env_wl","workflow_wl","test_wl", "vis_wl"]

wl_alias_names = ["programming langauges", "databases", "platforms", "misc tools",
                  "web frameworks","environments","workflow management","Testing Software",
                "visualization software" ]

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
                if outstring[-1] == " ":
                    outstring = outstring[:-1]
                outstring += '"'
            print(outstring)
        else:
            return None

 

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
    return job_entry


def check_lists(word,wl_names, white_lists):
    for i in range(0,len(wl_names)):
        if word in white_lists[i]:
            return wl_names[i]

def print_global_dict(gd,wl_alias):
    #print(gd)
    idx = 0
    for key, values in gd.items():
        if gd[key]:
            #if idx < len(wl_alias) + 1:
            print(wl_alias[idx].upper())
            for words, counts in values.items():
                print(words + "," + str(counts))
            print("\n")
        idx += 1

def print_job_entries(job_list, w_l_names):
    header = "jobid,"
    #print(job_list)
    for name in w_l_names:
        header += name + ","

    print(header[:-1])
    for job in job_list:
        out_string = job.print_data()
        if out_string:
            print(out_string)



def main(w_l_names,desc_path, w_l_aliases ):
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
                cur_job = digest(first_pass,w_l_names,white_lists,global_counts,cur_job)
                entry_list.append(cur_job)
                count += 1
            if count % 30 == 0:
                break


    print_job_entries(entry_list, w_l_aliases)
    print_global_dict(global_counts,w_l_aliases)


main(white_list_names,desc_file_path,wl_alias_names)

