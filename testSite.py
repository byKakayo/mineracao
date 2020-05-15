def site_strip(flag):
    dic_res = {}
    x = (flag - 1)*4
    y = numRes+1
    for i in range(x+1,y):
        j = int(str(i-x)+'7') + (i-x)
        dic_res[('resName'+str(i))] = line[j:(j+3)].strip()
        dic_res[('chainID'+str(i))] = line[(j+4)].strip()
        dic_res[('seq'+str(i))] = line[(j+5):(j+9)].strip()
    return dic_res
siteID = line[11:14].strip()
dic_res = {}
numRes = int(line[15:17].strip())
if numRes%4 == 0: flag = numRes//4
else: flag = ceil(numRes/4)
if tipo not in pdb_file:
    SITE = {}
    numRes = 4
    dic_res = site_strip(1)
    SITE[siteID] = dic_res
else:
    if siteID not in pdb_file[tipo]:
        numRes = 4
        dic_res = site_strip(1)
        SITE[siteID] = dic_res
    else:
        if (len(SITE[siteID])/12+1) == flag:
            dic_res = site_strip(flag)
        elif (len(SITE[siteID])/12+1) < flag:
            numRes = 4 * int(len(SITE[siteID])/12+1)
            dic_res = site_strip(int(len(SITE[siteID])/12+1))
        SITE[siteID].update(dic_res)
pdb_file[tipo] = SITE
