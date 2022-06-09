from chimerax.core.commands import run
"""
This file contains code to produce 2 tables. 
One is to view Rosetta energy scores for the entire protein.
The other is to view individual Rosetta scores for a each residue.
"""

"""
CODE to view Rosetta energy scores for the entire protein.
"""
def getLabelsAndWeights(fileName):
    #open the file
    with open(fileName) as f:
        lines = f.readlines()
        #i is the index of the line in the PDB file the reader is currently at
        #table_index is the index where the data begins
        i = -1
        table_index = -1
        for line in lines:
            i += 1
            if ("pose" in line.lower()) and ("table" in line.lower()):
                table_index = i
                break
    if (table_index != -1):
        labelList = lines[table_index+1].split() #string of space separated labels to list of labels
        weightsList = lines[table_index+2].split() #string of space separated weights to list of weights
        f.close()
        return labelList, weightsList

    else:
        f.close()
        print("Did not find where the table information is located in the document")

def makeWeightTable(filename, pdb_name):
    #initialize the two sections of the table
    table_header = "<tr>\n"
    table_rows = "<tr><td>" + pdb_name + "</td>\n"

    #retrieve the labelList and the weightslist
    labelList, weightsList = getLabelsAndWeights(filename)

    for i in labelList: #append labels to the header
        table_header += "<th>" + i + "</th>"

    table_header += "</tr>" #close off the table_header

    for j in weightsList[1:]: #add the weights to the row for that protein
        table_rows += "<td>" + j + "</td>"
    table_rows += "</tr>" #close off the table_rows

    table_string = "<table>" + table_header + table_rows + "</table>"

    log_command = "log html " + table_string 

    run(session, log_command)


"""
CODE to view individual Rosetta scores for a each residue.
"""
def separateRosFromPDB(txt): 
  rosetta_start = txt.find("Nterm") 
  rosetta_lines = txt[rosetta_start-4:].splitlines() 

  ter_indices = [i+3 for i in range(rosetta_start-4) if txt.startswith("TER", i)]
  pdb_start = txt.find("ATOM")
  pdb_lines = txt[pdb_start:ter_indices[-1]].splitlines() 
  return rosetta_lines, pdb_lines
  
#get separate rosetta chains from a list of rosetta lines
#returns: a list of list of strings, one chain = list of strings
#one string is a residue
def getRosChainList(rosetta_lines): 
  rosetta_chain_list = []
  start = -1
  end = -1
  for i in range(len(rosetta_lines)):
    line = rosetta_lines[i]
    terms = line.split()
    residue = terms[0]
  
    if "NtermProtein" in residue: #case we are starting a new amino acid
      start = i
    elif "CtermProtein" in residue:
      end = i
      rosetta_chain_list.append(rosetta_lines[start:end+1])
      start = i + 1
  return rosetta_chain_list
  
#iterate through and display the rosetta chains
def display_rosetta_chains(rosetta_chain_list):
  for i in rosetta_chain_list:
    for j in i:
      print(j[0:3], end = " ")
    print("")
  print("done printing rosetta chains")

#get separate PDB chains

def getPDBChainList(pdb_lines): 
  pdb_chain_list = []
  start = 0
  end = -1

  for i in range(len(pdb_lines)): #iterate through lines of PDB string list
    line = pdb_lines[i]
    if "TER" in line: #need to start new chain
      end = i 
      pdb_chain_list.append(pdb_lines[start:end]) #chain list does not include TER
      start = i + 1
      
  return pdb_chain_list

#iterate through and display the pdb chains
def printPDBChains(pdb_chain_list):
  for i in pdb_chain_list:
    for j in i: 
      terms = j.split()
      print(terms[3], end = " ")
    print("")
  print("done printing pdb ids")

def getResInfo(rosetta_chain_list, pdb_chain_list):
  for chain_index in range(len(rosetta_chain_list)):
    chain = rosetta_chain_list[chain_index]
    pdb_chain = pdb_chain_list[chain_index] #list of residues in string form for PDB 
    ros_chain = rosetta_chain_list[chain_index] #list of res in string form for PDB 
    pdb_res_row = pdb_chain[0].split()
    chain_label = pdb_res_row[4]
    pdb_res_num = pdb_res_row[5]
   
    ros_res_stats = ros_chain[0].split() #get the first residue then find the _
    ros_res_and_num = ros_res_stats[0]
    i = ros_res_and_num.find("_")
    ros_res_num = ros_res_and_num[i+1:]
    shift = int(pdb_res_num) - int(ros_res_num)
  
    for residue_row in chain:
      stats = residue_row.split() #list of all the terms in the row 
      residue = stats[0][:3] #name of the residue, always 3 chars long
      #if the res num is located later in start of chain
      if "termProteinFull" in stats[0]:  
        ros_res_and_num = stats[0]
        i = ros_res_and_num.find("_")
        ros_res_num = ros_res_and_num[i+1:]
        residue_number = int(ros_res_num) + shift
      else:  
        ros_res_and_num = stats[0]
        ros_res_num = ros_res_and_num[4:]
        residue_number = int(ros_res_num) + shift
      total_energy = stats[-1]
      print(chain_label, residue, residue_number, total_energy)
    print("\n")
  return

def makeResTableString(res_info_list):
  table_header = "<tr><td>Chain</td><td>Res</td><td>Res Nume</td><td>Total Energy</td></tr>"
  table_rows = ""

  for res_info in res_info_list: #add the weights to the row for that protein
    row_string = "<tr>"
    
    for entry in res_info: 
      row_string += "<td>" + str(entry) + "</td>"
    row_string += "</tr>" #close off the table_rows

    table_rows += row_string
  table_string = "<table>" + table_header + table_rows + "</table>"
  return table_string
    #run(session, log_command)
  
def makeResTable(filepath):
    #open the file
    with open(filepath) as f:
        txt = "".join(f.readlines())
  
    rosetta_lines, pdb_lines = separateRosFromPDB(txt) 
    rosetta_chain_list = getRosChainList(rosetta_lines)
    pdb_chain_list = getPDBChainList(pdb_lines)
  
    res_info = getResInfo(rosetta_chain_list, pdb_chain_list)
    table_string = makeResTableString(res_info)

    log_command = "log html " + table_string 
    
    run(session, log_command)
   
    f.close()
    #print(log_command)


makeWeightTable('/Users/sophieliu/Desktop/example.pdb', "example")
makeResTable("/Users/sophieliu/Desktop/direct_scripts/shorter.pdb")