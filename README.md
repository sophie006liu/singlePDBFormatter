# singlePDBFormatter
displays PDB info as a formatted table in the log section

1) you want to download "singlePDBTables.py" not singlePDBTables2.py, etc.
2) open chimeraX and type the command "open "PATH/singlePDBTables.py" " where PATH is the path to get to the source code
3) to generate the tables there are 3 options:
     i) makePdbTable FILEPATH (this displays general info about the protein: fa_atr, fa_rep, fa_sol,....)
     ii) makeResTable FILEPATH (this displays info for each residue in the protein: fa_atr, fa_rep, fa_sol,....)
     iii) makePdbAndResTable FILEPATH (runs both makePdbTable and makeResTable)
