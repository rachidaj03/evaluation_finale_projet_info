class person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

person1=person(1,45)
person2=person(2,89)
all_users = person.objects.all()