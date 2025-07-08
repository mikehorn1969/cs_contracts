# classes.py
# classes for use in cs_contracts app


class Config:

    _instances = []

    def __init__(self, key, value ):
        self.key = key
        self.value = value
        Config._instances.append(self)
        
    @classmethod
    def find_by_name(cls, search_name):
        for search_config in cls._instances:
            if search_config.key == search_name:
                return search_config.value
        return None


class Company:

    counter = 0
    _instances = []

    def __init__(self, companyname, address, email, phone, companyNumber  ):
        self.company_name = companyname
        self.address = address
        self.emailaddress = email
        self.phone = phone
        self.companyNumber = companyNumber
        Company.counter += 1 # increment the company counter
        Company._instances.append(self)

    @classmethod
    def count(cls):
        print(f"Company count: {cls.counter}")

    
    @classmethod
    def find_by_name(cls, search_name):
        for search_company in cls._instances:
            if search_company.name == search_name:
                return search_company
        return None
    

class Contact:

    counter = 0
    _instances = []

    def __init__(self, companyname, name, address, emailaddress, phone, title  ):        
        self.company_name = companyname
        self.name = name
        self.address = address
        self.emailaddress = emailaddress
        self.phone = phone
        self.title = title
        
        Contact.counter += 1 # increment the company counter
        Contact._instances.append(self)

    @classmethod
    def count(cls):
        print(f"Contact count: {cls.counter}")

    @classmethod
    def get_all_contacts(cls):
        return cls._instances
    
    @classmethod
    def find_by_name(cls, search_name):
        for search_contact in cls._instances:
            if search_contact.name == search_name:
                return search_contact
        return None    
    
    @classmethod
    def find_by_company(cls, search_company):
        contacts = []
        for search_contact in cls._instances:
            if search_contact.company_name == search_company:
                contacts.append(search_contact)
        
        if contacts is None:
            return None    
        else:
            return contacts
