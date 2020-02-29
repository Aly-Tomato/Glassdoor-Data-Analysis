import os,re, csv
from bs4 import BeautifulSoup
import langdetect

path = os.getcwd() + "/"

white_list_names = ["pl_wl","DB_wl","platforms_wl","tools_wl",
                    "web_Frame_wl","env_wl","workflow_wl","test_wl", "vis_wl"]

wl_alias_names = ["programming langauges", "databases", "platforms", "misc tools",
                  "web frameworks","environments","workflow management","Testing Software",
                "visualization software" ]

desc_file_path = "/Users/chrism/Data_sci/desc.csv"

edu_file = "ed_regex.txt"

out_file_name = "requirements_table.csv"


class descript:
    def __init__(self, _ID, _wl_list):
        self.ID = _ID
        self.min_degree = "unknown"

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

    def change_ed(self,edu):
        if self.min_degree == "unknown":
            self.min_degree = edu

    def get_id(self):
        return self.ID

    def get_list(self,category):
        items_list = self.lists_cats[category]
        fields = []
        for key,value in items_list.items():
            fields.append(key)
        return fields

    def print_data(self):
        if self.modified:
            outstring = self.ID
            outstring+="," + self.min_degree
            for key,values in self.lists_cats.items():
                outstring += ',"'
                for words, count in values.items():
                    outstring += words + " "
                if outstring[-1] == " ":
                    outstring = outstring[:-1]
                outstring += '"'
            return outstring
        else:
            return None


 

def load_white_list(wl_names):
    list_of_wl = []
    for name in wl_names:
        file_name = path + "white_lists/" + name + ".txt"
        wl_set = set()
        wl_file = open(file_name, 'r')
        for line in wl_file:
            line = line.strip()
            line = line.lower()
            wl_set.add(str(line.lower()))
        list_of_wl.append(wl_set)
    return list_of_wl

def load_edu(ed_file_name):
    ed_regexes = []
    ed_path = path + "white_lists/" + ed_file_name
    ed_file = open(ed_path, 'r')
    for line in ed_file:
        regex = re.compile(line)
        ed_regexes.append(regex)
    return ed_regexes




def make_global_count_dict(wl_names):
    global_dict = {}
    for wl_name in wl_names:
        temp = {wl_name: {'total':0}}
        global_dict.update(temp)
    return global_dict



def digest(desc,wl_names,wlists, global_counts, job_entry):
    desc = desc.replace('\n',' ')
    desc = desc.lower()
    desc_list = desc.split(' ')
    total_list = [False]*len(wl_names)
    found_words = set()
    for word in desc_list:

        cur_wl = check_lists(word.lower(),wl_names,wlists)
        if cur_wl:
            found_words.add((cur_wl,word.lower()))
    if found_words:
        found_list = list(found_words)
        for found in found_list:
            job_entry.add_term(found[0], found[1])
            temp = global_counts[found[0]]
            #print(found[0])
            if temp.get(found[1])== None:
                temp[ found[1]] = 1
            else:
                temp[ found[1]] += 1

            global_counts[found[0]] = temp
            idx = wl_names.index(found[0])
            total_list[idx] = True

        for i in range(0,len(wlists)):
            if total_list[i]:
                cur_wl = wl_names[i]
                temp = global_counts[cur_wl]
                temp["total"] += 1
    return job_entry


def check_lists(word,wl_names, white_lists):
    for i in range(0,len(wl_names)):
        if word in white_lists[i]:
            return wl_names[i]

def parse_ed(ed_strings,job_entry,edu_regex):
    for i in range (0,len(ed_strings)):
        edu = re.sub("[->,/\n]", ' ', ed_strings[i])
        edu = re.sub("[->\"%#/&$()?'!:*\t\[\]]", '', edu)
        desc = edu.replace('\n',' ')
        desc_list = desc.split(' ')
        ed_list = ["High School", "Associates", "Bachelors", "Masters", "PhD"]
        for word in desc_list:
            ed_code = capture_edu(word, edu_regex)
            if ed_code >= 0:
                #print(ed_code, ed_list[ed_code], job_entry.get_id())
                job_entry.change_ed(ed_list[ed_code])

def capture_edu(word,ed_reg):
    for i in range(0,len(ed_reg)):
        if ed_reg[i].match(word.lower()):
            return i
    return -1

def print_global_dict(gd,wl_alias):
    #print(gd)
    idx = 0
    for key, values in gd.items():
        temp = gd[key]
        if temp["total"] > 0:
            #if idx < len(wl_alias) + 1:
            print(wl_alias[idx].upper())
            for words, counts in values.items():
                print(words + "," + str(counts))
            print("\n")
        idx += 1

def write_global_dict(gd, wl_alias):
    idx = 0

    for key, values in gd.items():
        temp = gd[key]
        #print(key)
        if temp["total"] > 0:
            out_file = open(path + "/count_data/" + key[:-3] +"_count.txt", 'x')
            # if idx < len(wl_alias) + 1:
            out_file.write(wl_alias[idx].upper() +"\n")
            for words, counts in values.items():
                out_file.write(words + "," + str(counts) +"\n")
        idx += 1

def print_job_entries(job_list, w_l_names):
    header = "jobid,education,"
    #print(job_list)
    for name in w_l_names:
        header += name + ","
    print(header[:-1])
    for job in job_list:
        out_string = job.print_data()
        if out_string:
            print(out_string)

def write_job_entries(job_list, w_l_names,out_f_name):
    header = "jobid,education,"
    out_file = open(path + out_f_name, 'x')
    #print(job_list)
    for name in w_l_names:
        header += name + ","
    out_file.write(header[:-1] +"\n")
    for job in job_list:
        out_string = job.print_data()
        if out_string:
            out_file.write(out_string+"\n")

def gen_ed_list(ed_string, ed_cnt):
    if ed_string:
        ed_string = ed_string.replace('\n', ' ')
        ed_list = ed_string.split(' ')
        for word in ed_list:
            word = word.lower()
            count = ed_cnt.get(word.strip())
            if count == None:
                ed_cnt[word] = 1
            else:
                ed_cnt[word] += 1
    return ed_cnt

def print_ed_cnt(ed_cnt):
    for key,values in ed_cnt.items():
        print(key + "," + str(values))


def gen_one_hot_header(wlist):
    header = ["jobid"]
    for term in wlist:
        header.append(term)
    return header

def gen_hash_index(wl):
    idx = 1
    hash_idx = {}
    for word in wl:
        hash_idx[word] = idx
        idx += 1
    return hash_idx


def process_one_hot(all_jobs,w_lists,wl_names):

    #one_hots = [] * len(w_lists)
    wl_name_idx = 0

    # for each whitelist
    for list in w_lists:
        cur_one_hot = []
        # generate header
        header = gen_one_hot_header(list)
        cur_one_hot.append(header)
        #one_hots.append()
        # create index_hash
        cur_hi = gen_hash_index(list)
        for cur_job in all_jobs:
            # get fields from job for specific list
            field_list = cur_job.get_list(wl_names[wl_name_idx])
            if field_list:
                # create lists of 0s
                cur_row = [0]*(len(list) + 1)
                cur_row[0] = cur_job.get_id()
                #print(field_list)
                # use indexes from index_hash to
                for field in field_list:
                    #print(field)
                    #print(cur_hi)
                    temp = cur_hi[field]
                    cur_row[temp] = 1
                cur_one_hot.append(cur_row)
        write_onehot(cur_one_hot,wl_names[wl_name_idx])
        wl_name_idx += 1



def write_onehot(one_hot,out_f_name):

    out_file = open(path +"/onehots/" +out_f_name[:-3] +"_one_hots.csv", 'x')

    for row in range(0,len(one_hot)):
        out_str = ""
        for word in one_hot[row]:
            out_str += str(word) + ","
        out_str = out_str[:-1] + "\n"
        out_file.write(out_str)

    '''
    for name in w_l_names:
        header += name + ","
    out_file.write(header[:-1] +"\n")
    for job in job_list:
        out_string = job.print_data()
        if out_string:
            out_file.write(out_string+"\n")
'''







def main(w_l_names,desc_path, w_l_aliases ):
    entry_list = []
    global_counts = make_global_count_dict(w_l_names)
    white_lists = load_white_list(w_l_names)
    count = 0
    ed_count = {}
    ed_regexes = load_edu(edu_file)
    #print(ed_regexes[0]
    with open(desc_path, 'r') as csvfile:
        entries = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in entries:
            jobid = row["gaTrackerData.jobId"]
            cur_job = descript(jobid,w_l_names)
            desc_entry = row["job.description"]
            if langdetect.detect(desc_entry) == "en":
                soup = BeautifulSoup(desc_entry, "lxml")
                experience = soup.findAll(string=re.compile(r'[Dd]egree|[Dd]iploma|[Ee]ducation'))
                if experience:
                    #print(experience)

                    #print(edu)
                    parse_ed(experience,cur_job,ed_regexes)
                    #ed_count = gen_ed_list(edu,ed_count)
                #print(experience)
                first_pass = re.sub("[->,\"%#/&$().?'!:*\t\[\]]", ' ', soup.get_text(separator=' '))
                cur_job = digest(first_pass,w_l_names,white_lists,global_counts,cur_job)
                entry_list.append(cur_job)
                count += 1
            if count % 1000 == 0:
                print(str(count) + " number of records parsed")
                #break

    process_one_hot(entry_list,white_lists,w_l_names)
    #print_job_entries(entry_list, w_l_aliases)
    #write_job_entries(entry_list,w_l_aliases,out_file_name)
    #write_global_dict(global_counts,w_l_aliases)
    #print_global_dict(global_counts,w_l_aliases)
    #print_ed_cnt(ed_count)

main(white_list_names,desc_file_path,wl_alias_names)


