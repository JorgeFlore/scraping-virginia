
import csv 

def leer_csv():
    #with open("utils/credenciales_sii.csv", 'r') as file:
    with open("C:\\Scraping\\bci\\utils\\credenciales_sii.csv", 'r') as file:
        next(file)
        csv_reader = csv.reader(file)
        data_list = []

        for row in csv_reader:
            data_list.append(row)
    return data_list


def listar_correos():
    #correos =["manuel.rodriguez@aguasnuevas.cl","eduardo.gajardo@aguasnuevas.cl","orlando.sanmartin@aguasnuevas.cl","jorge.flores@aguasnuevas.cl","vania.moena@aguasnuevas.cl","ivan.zurita@aguasnuevas.cl"]
    #with open("utils/listado_mail.csv", 'r') as file:
    with open("C:\\Scraping\\bci\\utils\\listado_mail.csv", 'r') as file:
        next(file)
        csv_reader = csv.reader(file)
        email = []
        for row in csv_reader:
            email.append(row)
    
    
    return email
#for row in data_list:
#    print(row[0])
#    print(row[1])


#with open("utils/listado_mail.csv", 'r') as file:
#    next(file)
#    csv_reader = csv.reader(file)
#    email = []
#    for row in csv_reader:
#        email.append(row)
#print(email)


