def clean_str(somestr, remove):
    return somestr.translate({ord(i):None for i in f"{remove}"})

