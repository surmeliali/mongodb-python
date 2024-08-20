import json

def readJSONFile(config):

    json_file_name = config.get('data_files','json_file')
    # with open(load_file, 'r') as file:
    file = open(json_file_name)
    json_data = json.load(file)
    file.close()
    return json_data

# def showJsonFile(data):
#     for line in data:
#         print(line)