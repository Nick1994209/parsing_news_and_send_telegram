def prepare_list_dict(list_data):
    print(list_data)
    prepared_data = []
    for data in list_data:
        if isinstance(data, dict):
            prepared_data.append(prepare_dict(data))
        if isinstance(data, list):
            prepared_data.append(prepare_list_dict(data))
        else:
            prepared_data.append(data)

    print(prepared_data)
    return prepared_data


def prepare_dict(data):
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()
    return data
