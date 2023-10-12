import json

def readFileRJSON(filename):
    '''Reads a json file written by R to contain the time and frequency
    data for contours annotated in Pamguard. Returns a two dimensional
    Python list with tuples of (time, frequency), where both are a floating
    point value. eg. [[(1.2,75.23), (1.25, 74.77), (1.3, 74.26)], [(4.9,62.48), (5.52, 60.29)]]
    represents two contours, the first of which has three nodes and the second has two.'''
    with open(filename, 'r') as file:
        raw_data = json.load(file)

    data = []

    for contour in raw_data:
        time = contour["time"]
        freq = contour["freq"]
        data.append(list(zip(time, freq)))

    return data


def readAllFilesRJSON(filename):
    '''Reads a json file written by R to contain the time and frequency
    data for contours from multiple files annotated in Pamguard. Returns an array of
    dictionaries. Each dictionary has the field "filename," which contains
    the file path to the Pamguard binary file that originally contained the contours,
    and "data," which contains a two-dimensional Python list with tuples of (time, frequency),
    where both are a floating point value. 
    eg. [[(1.2,75.23), (1.25, 74.77), (1.3, 74.26)], [(4.9,62.48), (5.52, 60.29)]]
    represents two contours, the first of which has three nodes and the second has two.'''
    
    with open(filename, 'r') as file:
        raw_data = json.load(file)

    files = []
    for file in raw_data:
        new_dictionary = {
            "filename": file["filename"][0],
            "data": []
            }
        for contour in file["data"]:
            time = contour["time"]
            freq = contour["freq"]
            new_dictionary["data"].append(list(zip(time, freq)))

        files.append(new_dictionary)

    return files