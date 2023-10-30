from classes import Field, Name, Phone, AddressBook, Record, Birthday
import pickle
import re
def input_error(f):
    def inner(*args):
        try:
            return f(*args)
        except IndexError:
            return "Give me more data " 
        except KeyError:
            return 'User not in dict'
        except TypeError:
            return 'There is no such request'
        except AttributeError:
            return 'Not birthday'
    return inner

records = AddressBook()


@input_error
def add_record(*args):
    rec_id = args[0]
    rec_value = args[1]
    if rec_id in records.keys():
        return 'Users is empty'
    new_record = Record(rec_id) 
    new_record.add_phone(rec_value)
    records[rec_id] = new_record
    try:
        new_record.add_birthday(args[2])
    except IndexError:
        birthday = None
    print('_' * 30)
    return f'Contact {rec_id} successfully added'
    

@input_error
def change_record(*args):
    rec_id = args[0]
    old_phone = args[1]
    new_phone = args[2]
    records.find(rec_id).edit_phone(old_phone, new_phone)
    print('_' * 30)
    return f'Change {rec_id = }, {new_phone = }'


@input_error
def phone_record(*args):
    rec_id = args[0]
    if rec_id not in records:
        raise KeyError
    print('_' * 30)
    return f'{records.get(rec_id)}'


@input_error
def birthday_func(*args):
    rec_id = args[0]
    rec = records.get(args[0])
    if rec_id not in records:
        print('_' * 30)
        return f' Contact {rec_id} not in Notebook'
    else:
        print('_' * 30)
        return f'Birthday will be after {rec.days_to_birthday()} days'


def hello_func(*args):
    print('_' * 30)
    return 'How can I help you?'


@input_error
def show_all_func(*args):
    num = int(args[0])
    line = ''
    for res in records.iterator(num):
        line += res
    print('_' * 30)
    return line

@input_error
def find_person(*args):
    rec_id = args[0]
    string = ''
    for record in records.values():
        result = str(record.name)
        for phone in record.phones:
            result += str(phone)
        find = re.findall(rec_id, result)
        if len(find) > 0:
            string += f'{record}\n'
    if len(find) == 0:
        print('_' * 30)
        return 'No matches'
    print('_' * 30)
    return string



def unknown(*args):
    print('_' * 30)
    return 'Unknown command. Try again'


COMMANDS = {add_record: 'add',
            change_record: 'change',
            phone_record: 'phone',
            hello_func: 'hello',
            show_all_func: 'show all',
            birthday_func: 'birthday',  
            find_person: 'find' 
            }


def parser(text:str):
    for func, val in COMMANDS.items():
        if text.lower().startswith(val):
            return func, text[len(val):].strip().split()
    return unknown, []


def main():
    while True:
        user_input = input('>>>')
        if user_input.lower() == 'exit':
            book = AddressBook()
            book.save_file(records)
            print('Good bye')
            break
        try:
            get = AddressBook()
            records.update(get.get_file())
        except:
            'Not file'
        func, data = parser(user_input)
        print(func(*data))


if __name__ == '__main__':
    main()