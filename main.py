import re
import csv

def read_csv():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    contacts_json = []
    keys_list = contacts_list.pop(0)
    for values in contacts_list:
        temp_dict = {}
        for key in keys_list:
            temp_dict[key] = values[keys_list.index(key)]
        contacts_json.append(temp_dict)
    return contacts_json


def list_of_dicts_to_csv(list_dicts):
    return_list = []
    return_list.append(list_dicts[0].keys())
    for dict in list_dicts:
        return_list.append(dict.values())
    return return_list


def write_csv(list_strings):
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list_strings)


def phone_rewrite(phone_string):
    re_string = r'(\+7|8)?\s*\-?\(?(\d{3}){1}\)?\-?\s*(\d{3}){1}\-?\s*(\d{2}){1}\-?\s*(\d{2}){1}\s*\(?(доб\.?)?\s*(\d*)?\)?'
    new_phone = re.sub(re_string, r'+7(\2)\3-\4-\5\6\7', phone_string)

    return new_phone


def name_rewrite(dict):
    if dict['lastname'] and dict['firstname'] and dict['surname']:
        return dict
    else:
        temp_name = dict['lastname'] + ' ' + dict['firstname'] + ' ' + dict['surname']
        temp_list_name = temp_name.split(' ')
        dict['lastname'] = temp_list_name[0]
        dict['firstname'] = temp_list_name[1]
        dict['surname'] = temp_list_name[2]
    return dict


def dublicats(list_dicts):
    temp_names_list = []
    temp_dict_list = []
    for dict in list_dicts:
        temp_name = dict['lastname'] + ' ' + dict['firstname']
        if temp_name in temp_names_list:
            for k in dict.keys():
                if dict[k] == '':
                    dict[k] = temp_dict_list[temp_names_list.index(temp_name)][k]
            temp_dict_list.remove(temp_dict_list[temp_names_list.index(temp_name)])
            temp_names_list.remove(temp_name)
            temp_names_list.append(temp_name)
            temp_dict_list.append(dict)
        else:
            temp_names_list.append(temp_name)
            temp_dict_list.append(dict)
    return temp_dict_list


def main():
    dict_list_temp = read_csv()
    dict_list = []
    for dict in dict_list_temp:
        temp_dict = name_rewrite(dict)
        temp_dict['phone'] = phone_rewrite(temp_dict['phone'])
        dict_list.append(temp_dict)
    dict_list = dublicats(dict_list)
    write_csv(list_of_dicts_to_csv(dict_list))



if __name__ == '__main__':
    main()