from chimerax.core.commands import run

def printZippedLists(labelList, weightsList):
    #make sure each label has a weight and vice versa
    if len(labelList) != len(weightsList): 
        print("Labels do not match weights")
    else:
        for i in range(len(labelList)):
            print(labelList[i] + ": " + weightsList[i])

with open('/Users/sophieliu/Desktop/example.pdb') as f:
    lines = f.readlines()
    i = -1
    table_index = -1
    for line in lines:
        i += 1
        if ("pose" in line.lower()) and ("table" in line.lower()):
            table_index = i
            break
    
    try:
        labelList = lines[table_index+1].split() #string of space separated labels to list of labels
        weightsList = lines[table_index+2].split() #string of space separated weights to list of weights
    except:
        print("Did not find where the table information isin the document")

#make the string for the html table

table_labels = "<tr>\n"

table_row = "<tr>\n"

for i in labelList:
    table_labels += "<th>" + i + "</th>"
table_labels += "</tr>"

for j in weightsList[1:]:
    table_row += "<td>" + j + "</td>"
table_row += "</tr>"

table_string = "<table>" + table_labels + table_row + "</table>"

log_command = "log html " + table_string 

run(session, log_command)
#log thumb html <b>Toxin from <i>Bacillus thuringiensis</i></b>