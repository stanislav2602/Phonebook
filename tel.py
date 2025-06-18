from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)


def processing_full_name(contacts):
    for contact in contacts[1:]:
        if len(contact) > 5:
            phone = contact[5]
            phone = re.sub(r'(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})',
                           r'+7(\2)\3-\4-\5', phone)
            phone = re.sub(r'\(?доб\.?\s*(\d+)\)?', r'доб.\1', phone)
            contact[5] = phone

        full_name = ' '.join(contact[:3]).split()
        for i in range(len(full_name)):
            if i < 3:
                contact[i] = full_name[i]
        while len(contact) < 7:
            contact.append('')


def duplicates(contacts):
    unique_contacts = {}
    for contact in contacts[1:]:
        key = (contact[0], contact[1])
        if key in unique_contacts:
            existing_contact = unique_contacts[key]
            for i in range(len(contact)):
                if contact[i] and not existing_contact[i]:
                    existing_contact[i] = contact[i]
        else:
            unique_contacts[key] = contact
    return [contacts[0]] + list(unique_contacts.values())



processing_full_name(contacts_list)
contacts_list = duplicates(contacts_list)

with open("new_phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

print("Данные успешно обработаны и сохранены в файл new_phonebook.csv")