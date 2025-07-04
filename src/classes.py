# classes.py
# classes for use in cs_contracts app

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
        Company._instances.append(self) # track instance

    @classmethod
    def count(cls):
        print(f"Company count: {cls.counter}")

    @classmethod
    def get_all_companies(cls):
        return cls._instances
    
    @classmethod
    def find_by_name(cls, search_name):
        for search_company in cls._instances:
            if search_company.name == search_name:
                return search_company
        return None
    

class Contact:

    counter = 0
    _instsances = []

    def __init__(self, companyname, name, address, emailaddress, phone, title  ):        
        self.company_name = companyname
        self.name = name
        self.address = address
        self.emailaddress = emailaddress
        self.phone = phone
        self.title = title
        

        Contact.counter += 1 # increment the company counter

    @classmethod
    def count(cls):
        print(f"Contact count: {cls.counter}")

    @classmethod
    def get_all_companies(cls):
        return cls._instances
    
    @classmethod
    def find_by_name(cls, search_name):
        for search_contact in cls._instances:
            if search_contact.name == search_name:
                return search_contact
        return None    
    
    @classmethod
    def find_by_company(cls, search_company):
        for search_contact in cls._instances:
            if search_contact.name == search_company:
                return search_contact
        return None    
