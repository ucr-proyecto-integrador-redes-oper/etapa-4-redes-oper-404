import csv
 
with open('grafo_prueba.csv', newline='') as File:  
    reader = csv.reader(File)
    for row in reader:
        print(row)