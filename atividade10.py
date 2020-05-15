from math import ceil
#Inicializando dicionario
pdb_file = {}

#Criando listas para cada seção vide documentação:
#http://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html
#Title Section
title_sec = ["HEADER", "TITLE", "COMPND", "SOURCE", "KEYWDS", "EXPDTA", "AUTHOR", "REVDAT", "JRNL", "REMARK"]
#Primary Structure Section
prim_sec = ["DBREF", "SEQRES"]
#Heterogen Section
het_sec = ["HET", "HETNAM", "HETSYN", "FORMUL"]
#Secondary Structure Section
seco_sec = ["HELIX", "SHEET"]
#Crystallographic and Coordinate Transformation Section
crys_coord_transf_sec = ["CRYST1", "ORIGX1", "ORIGX2", "ORIGX3", "SCALE1", "SCALE2", "SCALE3"]
#Coordinate Section
coord_sec = ["ATOM", "HETATM"]

#Abrindo arquivo pdb
with open('1cls.pdb', 'r') as f:
    #Percorrendo linha a linha
    for line in f:
        line = line[:-1]
        tipo = line.split()[0]
        #Title Section
        if tipo in title_sec:
            if tipo == "HEADER":
                HEADER = {}
                HEADER['classification'] = line[10:50].strip()
                HEADER['date'] = line[50:62].strip()
                HEADER['ID'] = line[62:].strip()
                pdb_file[tipo] = HEADER
            elif tipo == "COMPND" or tipo == "SOURCE":
                line = line.replace(';', "")
                if tipo not in pdb_file:
                    pdb_file[tipo] = {}
                if ":" in line:
                    txt = line[10:].split(":")
                    key = txt[0].strip()
                    txt = txt[1].strip().split(",")
                    pdb_file[tipo][key] = txt
                else:
                    txt = line[10:].strip().split(",")
                    pdb_file[tipo][key] += txt
            elif tipo == "AUTHOR":
                list_author = []
                AUTHOR = {}
                if tipo not in pdb_file:
                    list_author = line[10:79].split(",")
                else:
                    list_author = pdb_file[tipo]
                    if list_author[-1] == "":
                        del list_author[-1]
                        list_author += line[10:79].split(",")
                    else:
                        aux = line[10:79].split(",")
                        list_author.append(list_author[-1] + aux[0])
                        del aux[0]
                        list_author += aux
                pdb_file[tipo] = list_author
            elif tipo == "REVDAT":
                list_rev = []
                REVDAT = {}
                if tipo in pdb_file:
                    list_rev = pdb_file[tipo]
                REVDAT['modNum'] = line[7:10].strip()
                REVDAT['modDate'] = line[13:22].strip()
                REVDAT['modId'] = line[23:27].strip()
                REVDAT['modType'] = line[31].strip()
                REVDAT['modDetail'] = line[40:].strip()
                list_rev.append(REVDAT)
                pdb_file[tipo] = list_rev
            elif tipo == "JRNL":
                sub_rec = line.split()[1]
                if tipo not in pdb_file:
                    pdb_file[tipo] = {}
                    pdb_file[tipo][sub_rec] = line[19:].strip()
                else:
                    if sub_rec in pdb_file[tipo]:
                        pdb_file[tipo][sub_rec] += line[19:].strip()
                    else:
                        pdb_file[tipo][sub_rec] = line[19:].strip()
            elif tipo == "REMARK":
                remark_num = line[7:10].strip()
                idk = line[11:].strip()
                if tipo not in pdb_file:
                    REMARK = {}
                    REMARK[remark_num] = idk
                else:
                    if remark_num in pdb_file[tipo] and idk != '':
                        pdb_file[tipo][remark_num] += " " + idk
                    else:
                        REMARK[remark_num] = idk
                pdb_file[tipo] = REMARK
            else:
                idk = line[10:].strip()
                if tipo not in pdb_file:
                    pdb_file[tipo] = idk
                else:
                    pdb_file[tipo] += idk
        #Primary Structure Section
        if tipo in prim_sec:
            if tipo == "DBREF":
                DBREF = {}
                if tipo not in pdb_file:
                    pdb_file[tipo] = {}
                DBREF['idCode'] = line[7:11].strip()
                chainID = line[12].strip()
                DBREF['seqBegin'] = line[14:18].strip()
                DBREF['seqEnd'] = line[20:24].strip()
                DBREF['database'] = line[26:32].strip()
                DBREF['dbAccession'] = line[33:41].strip()
                DBREF['dbIdCode'] = line[42:54].strip()
                DBREF['dbSeqBegin'] = line[55:60].strip()
                DBREF['dbSeqEnd'] = line[62:67].strip()
                DBREF['listRes'] = []
                pdb_file[tipo][chainID] = DBREF
            elif tipo == "SEQRES":
                chainID = line[11].strip()
                listRes = line[19:].split()
                pdb_file['DBREF'][chainID]['listRes'] += listRes
        #Heterogen Section
        if tipo in het_sec:
            if tipo == "HET":
                list_het = []
                HET = {}
                if tipo in pdb_file:
                    list_het = pdb_file[tipo]
                HET['hetID'] = line[7:10].strip()
                HET['chainID'] = line[12].strip()
                HET['seqNum'] = line[13:17].strip()
                HET['numHetAtoms'] = line[20:25].strip()
                HET['txt'] = line[30:].strip()
                list_het.append(HET)
                pdb_file[tipo] = list_het
            elif tipo == "HETNAM":
                het_id = line[11:14].strip()
                txt = line[15:].strip()
                if tipo not in pdb_file:
                    HETNAM = {}
                    HETNAM[het_id] = txt
                else:
                    if het_id in pdb_file[tipo]:
                        pdb_file[tipo][het_id] += " " + txt
                    else:
                        HETNAM[het_id] = txt
                pdb_file[tipo] = HETNAM
            elif tipo == "HETSYN":
                hetID = line[11:14].strip()
                if tipo not in pdb_file:
                    pdb_file[tipo] = {}
                    pdb_file[tipo][hetID] = line[15:].split()
                else:
                    if hetID in pdb_file[tipo]:
                        pdb_file[tipo][hetID] += line[15:].split()
                    else:
                        pdb_file[tipo][hetID] = line[15:].split()
            elif tipo == "FORMUL":
                list_formul = []
                FORMUL = {}
                if tipo in pdb_file:
                    list_formul = pdb_file[tipo]
                FORMUL['compNum'] = line[8:10].strip()
                FORMUL['hetID'] = line[12:15].strip()
                FORMUL['asterisk'] = line[18].strip()
                FORMUL['txt'] = line[19:].strip()
                list_formul.append(FORMUL)
                pdb_file[tipo] = list_formul
        #Secondary Structure Section
        if tipo in seco_sec:
            if tipo == "HELIX":
                list_helix = []
                HELIX = {}
                if tipo in pdb_file:
                    list_helix = pdb_file[tipo]
                HELIX['serNum'] = line[7:11].strip()
                HELIX['helixID'] = line[11:14].strip()
                HELIX['initResName'] = line[15:18].strip()
                HELIX['initChainID'] = line[19].strip()
                HELIX['initSeqNum'] = line[21:25].strip()
                HELIX['endResName'] = line[27:30].strip()
                HELIX['endChainID'] = line[31].strip()
                HELIX['endSeqNum'] = line[33:37].strip()
                HELIX['helixClass'] = line[38:40].strip()
                HELIX['comment'] = line[40:70].strip()
                HELIX['length'] = line[71:76].strip()
                list_helix.append(HELIX)
                pdb_file[tipo] = list_helix
            elif tipo == "SHEET":
                strand = int(line[7:10].strip())
                sheetID = line[11:14].strip()
                STRAND = {}
                SHEET = {}
                STRAND['initResName'] = line[17:20].strip()
                STRAND['initChainID'] = line[21].strip()
                STRAND['initSeqNum'] = line[22:26].strip()
                STRAND['endResName'] = line[28:31].strip()
                STRAND['endChainID'] = line[32].strip()
                STRAND['endSeqNum'] = line[33:37].strip()
                SHEET[strand] = STRAND
                if tipo not in pdb_file:
                    pdb_file[tipo] = {}
                    pdb_file[tipo][sheetID] = SHEET
                if strand != 1:
                    SHEET[strand]['sense'] = 'parallel' if int(line[38:40].strip())==1 else 'anti-parallel'
                    SHEET[strand]['curAtom'] = line[41:45].strip()
                    SHEET[strand]['curResName'] = line[45:48].strip()
                    SHEET[strand]['curChainId'] = line[49].strip()
                    SHEET[strand]['curResSeq'] = line[50:54].strip()
                    SHEET[strand]['prevAtom'] = line[56:60].strip()
                    SHEET[strand]['prevResName'] = line[60:63].strip()
                    SHEET[strand]['prevChainId'] = line[64].strip()
                    SHEET[strand]['prevResSeq'] = line[65:69].strip()
                    pdb_file[tipo][sheetID].update(SHEET)
                else:
                    pdb_file[tipo][sheetID] = SHEET
        #Connectivity Annotation Section
        if tipo == "LINK":
            list_link = []
            LINK = {}
            if tipo in pdb_file:
                list_link = pdb_file[tipo]
            LINK['name1'] = line[12:16].strip()
            LINK['resName1'] = line[17:20].strip()
            LINK['chainID1'] = line[21].strip()
            LINK['resSeq1'] = line[22:26].strip()
            LINK['name2'] = line[42:46].strip()
            LINK['resName2'] = line[47:50].strip()
            LINK['chainID2'] = line[51].strip()
            LINK['resSeq2'] = line[52:56].strip()
            LINK['sym1'] = line[59:65].strip()
            LINK['sym2'] = line[66:72].strip()
            LINK['len'] = line[73:78].strip()
            list_link.append(LINK)
            pdb_file[tipo] = list_link
        #Miscellaneous Features Section
        if tipo == "SITE":
            def site_strip(flag):
                dic_res = {}
                x = (flag - 1)*4
                for i in range(x+1,numRes+1):
                    j = int(str(i-x)+'7') + (i-x)
                    dic_res[i] = {}
                    dic_res[i]['resName'] = line[j:(j+3)].strip()
                    dic_res[i]['chainID'] = line[(j+4)].strip()
                    dic_res[i]['seq'] = line[(j+5):(j+9)].strip()
                return dic_res
            flag = int(line[7:10].strip())
            siteID = line[11:14].strip()
            numRes = int(line[15:17].strip())
            dic_res = {}
            if tipo not in pdb_file:
                SITE = {}
                if numRes > 4: numRes = 4
                dic_res = site_strip(flag)
                SITE[siteID] = dic_res
            else:
                if siteID not in pdb_file[tipo]:
                    if numRes > 4: numRes = 4
                    dic_res = site_strip(flag)
                    SITE[siteID] = dic_res
                else:
                    if ceil(numRes/4) > flag: numRes = 4 * flag
                    dic_res = site_strip(flag)
                    SITE[siteID].update(dic_res)
            pdb_file[tipo] = SITE
        #Crystallographic and Coordinate Transformation Section
        if tipo in crys_coord_transf_sec:
            if tipo == "CRYST1":
                CRYST1 = {}
                CRYST1['a'] = line[6:15].strip()
                CRYST1['b'] = line[15:24].strip()
                CRYST1['c'] = line[24:33].strip()
                CRYST1['alpha'] = line[33:40].strip()
                CRYST1['beta'] = line[40:47].strip()
                CRYST1['gamma'] = line[47:54].strip()
                CRYST1['sGroup'] = line[55:66].strip()
                CRYST1['z'] = line[66:70].strip()
                pdb_file[tipo] = CRYST1
            else:
                DICT = {}
                DICT['v1'] = line[10:20].strip()
                DICT['v2'] = line[20:30].strip()
                DICT['v3'] = line[30:40].strip()
                DICT['t'] = line[45:55].strip()
                pdb_file[tipo] = DICT
        #Coordinate Section
        if tipo in coord_sec:
            ATOM = {}
            res = []
            resSeq = line[22:26].strip()
            if tipo in pdb_file and resSeq in pdb_file[tipo]:
                res = pdb_file[tipo][resSeq]
            if tipo not in pdb_file:
                pdb_file[tipo] = {}
            ATOM['serial'] = line[6:11].strip()
            ATOM['name'] = line[12:16].strip()
            ATOM['altLoc'] = line[16].strip()
            ATOM['resName'] = line[17:20].strip()
            ATOM['chainID'] = line[21].strip()
            ATOM['x'] = line[30:38].strip()
            ATOM['y'] = line[38:46].strip()
            ATOM['z'] = line[46:54].strip()
            ATOM['occ'] = line[54:60].strip()
            ATOM['tempFac'] = line[60:66].strip()
            ATOM['element'] = line[76:78].strip()
            res.append(ATOM)
            pdb_file[tipo][resSeq] = res
        #Connectivity Section
        if tipo == "CONECT":
            id_conect = line[6:11].strip()
            serial_number = line[11:].strip()
            if tipo not in pdb_file:
                CONECT = {}
                CONECT[id_conect] = serial_number
            else:
                if id_conect in pdb_file[tipo]:
                    pdb_file[tipo][id_conect] += " " + serial_number
                else:
                    CONECT[id_conect] = serial_number
            pdb_file[tipo] = CONECT
        #Bookkeeping Section
        if tipo == "MASTER":
            MASTER = {}
            MASTER['numRemark'] = line[10:15].strip()
            MASTER['idk("0")'] = line[15:20].strip()
            MASTER['numHet'] = line[20:25].strip()
            MASTER['numHelix'] = line[25:30].strip()
            MASTER['numSheet'] = line[30:35].strip()
            MASTER['numTurn'] = line[35:40].strip()
            MASTER['numSite'] = line[40:45].strip()
            MASTER['numXform'] = line[45:50].strip()
            MASTER['numCoord'] = line[50:55].strip()
            MASTER['numTer'] = line[55:60].strip()
            MASTER['numConect'] = line[60:65].strip()
            MASTER['numSeq'] = line[65:].strip()
            pdb_file[tipo] = MASTER
print(pdb_file)
