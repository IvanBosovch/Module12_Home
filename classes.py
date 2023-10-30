from collections import UserDict
from datetime import datetime, date
import pickle


class Field:
    def __init__(self, value:str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value      

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value


class Phone(Field):
    def __init__(self, value:str):
        self._value = None
        self.value = value
        
    @property
    def value(self):
        return self._value
        
    @value.setter
    def value(self, value: str):
        if len(value) != 10 or not value.isdigit():
            raise ValueError
        self._value = value   


class Birthday(Field):
    def __init__(self, birthday:str):
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday
    
    @birthday.setter
    def birthday(self, birthday: str):
        if birthday:
            try:
                self.__birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError('Not correct birthday')
        else:
            return 'No BD'


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)       
        self.phones = []
        self.birthday = Birthday(birthday)
        self.string = ''
       
    def add_phone(self, phone_add):
        self.phones.append(Phone(phone_add))
        x = [str(lt) for lt in self.phones]

    def add_birthday(self, birthday: Birthday):
        if birthday:
            self.birthday = Birthday(birthday)
       
    def remove_phone(self, phone_remove):
        self.phones.remove(self.find_phone(phone_remove))

    def find_phone(self, phone_find):
        for x in self.phones:
            if x.value == phone_find:
                return x

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone) in self.phones:
            lst_phones = [str(lt) for lt in self.phones]
            phone_index = lst_phones.index(old_phone)
            self.phones[phone_index] = Phone(new_phone)
        else: 
            raise ValueError
        
    def days_to_birthday(self):
        current_today = date.today()
        bday = self.birthday.birthday
        birth = bday.replace(year=current_today.year)
        dif_date = birth - current_today
        if dif_date.days > 0:
            return dif_date.days
        else:
            birth = bday.replace(year=current_today.year + 1)
            dif_date = birth - current_today
            return dif_date.days
        
        
    def __repr__(self):
        if self.birthday.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.birthday}"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            return record

    def delete(self, name):
        if name in self.data.keys():
            self.data.pop(name)
            return f'{name} delete!'
        
    def find(self, find_name) -> Record:
            if find_name in self.data.keys():
                return self.get(find_name)
    
    def iterator(self, n=2):
        num = 0
        result = '\n'
        for k, v in self.data.items():
            result += f'{v}\n'
            num += 1
            if num >= n:
                yield result
                result = '\n'
                num = 0
        yield result

    def save_file(self, records):
        with open('file.txt', 'wb') as fh:
            pickle.dump(records, fh)
        return 'Saving succesfully'

    def get_file(self):
        with open('file.txt', 'rb') as fh:
            result = pickle.load(fh)
            return result




