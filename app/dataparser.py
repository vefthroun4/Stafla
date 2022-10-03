import requests
import json
import re
import os

HONNUNARBRAUT_URL = "https://namskra.is/programmes/445598c8-b8c8-4287-83b8-ff773e0a2cab/json"
BOKBAND_URL = "https://namskra.is/programmes/b09385f2-d312-4eed-94f9-256e6cf45708/json"
TOLVUBRAUT_URL = "https://namskra.is/programmes/1878c334-b82b-4375-a174-efe5fe92f300/json"
TOLVUBRAUT2_URL = "http://tolvubraut.is/assets/tbr/afangar.json"
REQUIRES = "abbreviation"
TRUNCATE_KEYS = set([
    "former_schools",
    "exemplary",
    "abbreviation_version",
    "continued_education",
    "instructions",
    "coauthors",
    "status_trans",
    "status",
    "embedded_subject",
    "categorization_suggestion",
    "embedded_topics",
    "topics",
    "_id",
    "author"
])

class DataParser():
    def __init__(self, data=None, file=None, json_url=None, output_file="data.json"):
        """ Parses json data from a provided file or URL that returns JSON data """
        self.file = file
        self.json_url = json_url
        self.data = data
        self.output_file = output_file

        # Default to using Tölvubraut from Namskra
        if not self.file and not self.json_url and not self.data:
            self.json_url = TOLVUBRAUT_URL

        # Pattern that matches course names that match this format: VESM2VT05BU
        self.COURSE_PATTERN = r"[\u0041-\u00ff]+\d+[\u0041-\u00ff]+\d+[\u0041-\u00ff]*"

        self.save_to_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"instance\\{self.output_file}"))

        # Grab data from url or file if data is not explicitly provided
        if not self.data:
            self.set_data()

    def set_data(self, data=None):
        """ 
            Sets data to provided data or

            fetches it from a filepath to a json file or 
            
            gets json with a request from a url depending on which is provided.
        """
        if data:
            self.data = data
        else:
            if self.file:
                with open(self.file, "r") as f:
                    self.data = json.load(f)
            elif self.json_url:
                self.data = requests.get(self.json_url).json()

    def get_data(self):
        return self.data   
    
    def truncate_data(self, data=None, truncate_keys=set([]), requires=None):
        """ Deep clones a nested object

        Performs a deep clone of a nested object 
        and removes keys specified in truncate_keys

        Also if requires is specified it removes any object
        that does not contain the specified key
        """
        if not data:
            data = self.get_data()

        def inner(data):
            if isinstance(data, dict):
                new_dict = {}
                for k, v in data.items():
                    if k not in truncate_keys:
                        if isinstance(v, (dict, list)):
                            temp = yield from inner(v)
                            if temp:
                                new_dict[k] = temp
                        else:
                            new_dict[k] = v
                            
                if new_dict:
                    if requires:
                        if requires in new_dict:
                            yield new_dict
                    else:
                        yield new_dict

            elif isinstance(data, list):
                new_list = []
                for n in data:
                    if isinstance(n, (list, dict)):
                        temp = yield from inner(n)             
                        if temp:
                            new_list.append(temp)
                if new_list:
                    yield new_list
        self.data = list(inner(data))

    def fix_prerequisites(self, data=None):
        """ Formats prerequisite fields correctly """
        p = "prerequisites"
        for entry in data if data else self.data:
            if "einingar" in entry[p]:
                einingar, level = re.findall("\d+", entry[p])
                entry[p] = {"level":level, "einingar":einingar, "subject_name" : entry["abbreviation"][:4]}
            elif "samhli\u00f0a" in entry[p]:
                entry[p] = {"courses": [entry[p].split("(")[0].strip()], "simultaneous":True}
            else:
                entry[p] = {"courses" : re.findall(self.COURSE_PATTERN, entry[p])}
    
    def write_to_json(self, filepath=None):
        path = filepath if filepath else self.save_to_path
        with open(path, "w") as f:
            json.dump(self.get_data(), f, indent=2)


    def rename_keys(self, rename_keys={}):
        for entry in self.data:
            for k in rename_keys:
                entry[rename_keys[k]] = entry.pop(k) 

    def add_keys(self, add_on_match={}, key_to_add={}):
        """ 
        Looks for a k:v pair and on matching a key with a specified value
        it then updates the dictionary with key_to_add.
        
        If add_on_match is not specified, it will add key_to_add to every dict item
        
        Example usecase:

        dataparser_instance.add_keys(
        { # add_on_match
            "course_number" : [
                "ÍSLE3NB05(CT)",
                "ÍSLE3LF05(CT)", 
                "ÍSLE3BF05(CT)"
            ]
        },
        { # key_to_add
            "group" : {
                "courses" : [
                    "ÍSLE3NB05(CT)", 
                    "ÍSLE3LF05(CT)", 
                    "ÍSLE3BF05(CT)"
                ],
                "credits_required" : 10
            }
        })
        This will look for any matches to course_number and the keys in the list given
        and add group: {...} to the existing dict object being iterated upon.
        """

        for entry in self.data:
            for k, v in add_on_match.items():
                if isinstance(v, (list, tuple)):
                    if k in entry and entry[k] in v:
                        for k, v in key_to_add.items():
                            entry[k] = v    
                        continue
                else:
                    if k in entry and entry[k] == v:
                        for k, v in key_to_add.items():
                            entry[k] = v    
                        continue


    def main(self, requires=None, truncate=None):
        """ Automatically fetches data, cleans it up and then saves it"""
        self.truncate_data(requires=requires, truncate_keys=truncate)
        self.fix_prerequisites()
        self.write_to_json()


if __name__ == "__main__":
    parser = DataParser()
    parser.main(requires=REQUIRES, truncate=TRUNCATE_KEYS)
    



