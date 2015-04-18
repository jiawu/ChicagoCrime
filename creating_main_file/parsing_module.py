def read_data(file_name):
    """Functions should have docstrings explaining their use succinctly."""
    file_object = open(file_name,"r")
    file_data = file_object.readlines()
    header_list = file_data.pop(0).strip().split(",")
    data_list = []
    for data in file_data:
        data_list.append(data.strip().split(","))
    return((header_list,data_list))