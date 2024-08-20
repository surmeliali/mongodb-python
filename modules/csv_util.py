import csv

def readCSVFile(config):
    load_file = config.get('data_files','csv_file')
    
    # Make a list to keep the file contents
    fileContents = []

    with open(load_file, 'r') as file:
        csv_contents = csv.reader(file)
        for c in csv_contents:
            fileContents.append(c)
    
    return fileContents

def showCSVFile(contents):
    for line in contents:
        print(line)
