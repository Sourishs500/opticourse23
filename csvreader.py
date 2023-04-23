import pandas as pd

dept = "Electrical and Computer Engineering"

df = pd.read_csv("ECE_HTML_Courses.csv")

raw = df['0'].values.tolist()

# format list elements - raw contains mostly formatted course elements
raw=[ i.replace("<h3>", "") for i in raw]
raw=[ i.replace("</h3>", "\n") for i in raw]
raw=[ i.replace("<p>", "") for i in raw]
raw=[ i.replace("</p>", "\n") for i in raw]
li=[ i + "\n" for i in raw]

courselist=[ i[:i.find("\n")] for i in li ]

# omit course name
raw=[ i.replace(i, i[1 + i.find("\n"):]) for i in li]

unitcounts=[ i[7:i.find("\n")] for i in raw ]

# omit unit count
raw=[ i.replace(i, i[1 + i.find("\n"):]) for i in raw]

# raw contains description only

# final requisites list
requisites = []

# temp reqs
reqs = []

# temp coreqs
coreqs = []

s = ""
for i in range(len(raw)):
    s = raw[i]
    ind = s.find("equisite")
    if (ind == -1):
        reqs.append("")
        coreqs.append("")
    else:
        ind = s.find(":")
        if (ind != -1):
            s = s[ind + 2:]
            reqs.append(s[:s.find(".")])
        else:
            reqs.append("")

        s = s[s.find(".") + 2:]
        ind = s.find("equisite")

        if (ind == -1):
            coreqs.append("")
        else:
            ind = s.find(":")
            if (ind == -1):
                coreqs.append("")
            else:
                s = s[ind + 2:]
                coreqs.append(s[:s.find(".")])

for i in range(len(reqs)):
    if (len(coreqs[i]) != 0):
        reqs[i] = reqs[i] + ", "
    requisites.append(reqs[i] + coreqs[i])

for i in range(len(requisites)):
    if len(requisites[i])>1:
        requisites [i] = [k.replace(",", "") for k in requisites[i].split()]
        #for j in len(requisites[i]):
        
            
        if (requisites[i][0]=="course"):
            if True in [m.isnumeric() for m in requisites[i][1]]:
                requisites[i][0] = dept
        elif requisites[i][0]=="courses":
            if True in [m.isnumeric() for m in requisites[i][1]]:
                requisites[i][0] = dept
            if len(requisites[i])>=4:
                requisites[i][3] = dept+" "+requisites[i][3]
        requisites[i] = " ".join(requisites[i])
            
            #for j in range(1, len(requisites[i])):
            
        
        #["course","M31B","is","a","good","course","to","know"]
        

finaldf = pd.DataFrame(list(zip(courselist, unitcounts, requisites, li)), columns=['Course Title', 'Unit Count', 'Requisites', 'Course Description'])
finaldf["Requisites"] = finaldf["Requisites"].apply(lambda x: x.strip().rstrip())

finaldf.to_csv(dept + ".csv")