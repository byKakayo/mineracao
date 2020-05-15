# Lendo .pdb

pdb_file = {}

with open('5rgk.pdb', 'r') as f:
    for line in f:
        line = line[:-1]
        print(len(line), line)
        tipo = line[:10]
        print(tipo)
        if 'HEADER' in tipo:
            idk = line[10:50].strip()
            data = line[50:62].strip()
            codigo = line[62:].strip()
            print('\t'+tipo, idk, data, codigo, sep='\n\t')
            pdb_file['idk'] = idk
            pdb_file['data'] = data
            pdb_file['codigo'] = codigo
        elif 'TITLE' in tipo:
            nome = line[10:].strip()
            print('\t'+tipo, nome, sep='\n\t')
            if 'nome' not in pdb_file:
                pdb_file['nome'] = nome
            else:
                pdb_file['nome'] += nome
        else:
            break
print(pdb_file)


# Lendo .pdb

pdb_file = {}

with open('5rgk.pdb', 'r') as f:
    for line in f:
        line = line[:-1]
        type = line.split()[0]
        if 'HEADER' in type:
            idk = line[10:50].strip()
            date = line[50:62].strip()
            id = line[62:].strip()
            pdb_file['idk'] = idk
            pdb_file['date'] = date
            pdb_file['id'] = id
        elif 'TITLE' in type:
            title = line[10:].strip()
            if 'title' not in pdb_file:
                pdb_file['title'] = title
            else:
                pdb_file['title'] += title
        elif 'COMPND' in type:
            compound = line[10:].strip()
            if 'compound' not in pdb_file:
                pdb_file['compound'] = compound
            else:
                pdb_file['compound'] += compound
        elif 'SOURCE' in type:
            source = line[10:].strip()
            if 'source' not in pdb_file:
                pdb_file['source'] = source
            else:
                pdb_file['source'] += source
        elif 'KEYWDS' in type:
            keywds = line[10:].strip()
            if 'keywds' not in pdb_file:
                pdb_file['keywds'] = keywds
            else:
                pdb_file['keywds'] += keywds
        elif 'EXPDTA' in type:
            technique = line[10:].strip()
            if 'technique' not in pdb_file:
                pdb_file['technique'] = technique
            else:
                pdb_file['technique'] += technique
        elif 'AUTHOR' in type:
            authorList = line[10:].strip()
            if 'authorList' not in pdb_file:
                pdb_file['authorList'] = authorList
            else:
                pdb_file['authorList'] += authorList
        elif 'REVDAT' in type:
        else:
            break
print(pdb_file)
