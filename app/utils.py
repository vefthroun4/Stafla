def clean_str(somestr, remove):
    """ Truncates characters from string """
    return somestr.translate({ord(i):None for i in f"{remove}"})

