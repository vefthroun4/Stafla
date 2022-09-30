import requests
import json
import re
import os

test_url = "https://namskra.is/programmes/1c886af0-e2ef-4c05-bf3b-368e10b3483d/json"
HONNUNARBRAUT_URL = "https://namskra.is/programmes/445598c8-b8c8-4287-83b8-ff773e0a2cab/json"
TS_URL = "https://namskra.is/programmes/1878c334-b82b-4375-a174-efe5fe92f300/json"
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
    def __init__(self, data=None, file=None, json_url=None, save_to_path=None):
        """ Parses json data from a provided file or URL that returns JSON data """
        self.file = file
        self.json_url = json_url
        self.data = data
        if not self.file and not self.json_url and not self.data:
            self.json_url = TS_URL

        # Pattern that matches course names that match this format: VESM2VT05BU
        self.COURSE_PATTERN = r"[\u0041-\u00ff]+\d+[\u0041-\u00ff]+\d+[\u0041-\u00ff]*"

        self.save_to_path = save_to_path if save_to_path else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "instance\\data.json"))

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
    
    def truncate_data(self, data=None, truncate_keys={}, requires=None):
        """ Deep clones a nested object

        Performs a deep clone of a nested object 
        and removes keys specified in truncate_keys

        Also if requires is specified it removes any object
        that does not contain the specified key
        """
        if not requires:
            requires = REQUIRES

        if not truncate_keys:
            truncate_keys = TRUNCATE_KEYS

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

    def main(self):
        """ Automatically fetches data, cleans it up and then saves it"""
        self.truncate_data()
        self.fix_prerequisites()
        self.write_to_json()

    

if __name__ == "__main__":
    parser = DataParser()
    parser.main()
