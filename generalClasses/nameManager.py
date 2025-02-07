"""Class for all functions about unique names"""

#generates a uniqueName in from the dictionary
def generate_uniqueName(base_name: str, dic: dict):
    # If base_name already unique return base_name
    if base_name not in dic:
        return base_name
    
    count = 2
    new_name = f"{base_name} {count}"
    while new_name in dic:
        count += 1
        new_name = f"{base_name} {count}"

    return new_name



