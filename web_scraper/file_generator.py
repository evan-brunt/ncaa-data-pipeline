import json


def add_list_to_file(data, file_name):
    f = open(file_name, "w")
    for datum in data:
        f.write(json.dumps(datum) + "\n")
    f.close()
