from faker import Factory
from faker.providers import BaseProvider
from datetime import datetime

fake = Factory.create('en_GB')


class FamilyProvider(BaseProvider):
    def family(self, seed, size, injection=[]):
        fake.seed(seed)
        if len(injection) == 0:
            parents = [self.family_member(sex='M'),
                       self.family_member(sex='F')]
            children = []
            for _ in range(0, size - 2):
                a_child = self.family_member(
                    sex=fake.random.choice(['M', 'F']))
                children.append(a_child)
        else:
            if injection[0] == 'parents':
                parents = [self.family_member(sex='M'),
                           self.family_member(sex='F')]
                children = [injection[1]]
                for _ in range(0, size - 3):
                    a_child = self.family_member(
                        sex=fake.random.choice(['M', 'F']))
                    children.append(a_child)
            else:
                if injection[1]['sex'] == 'M':
                    parents = [injection[1],
                               self.family_member(sex='F')]
                else:
                    parents = [injection[1],
                               self.family_member(sex='M')]
                children = []
                for _ in range(0, size - 2):
                    a_child = self.family_member(
                        sex=fake.random.choice(['M', 'F']))
                    children.append(a_child)
        a_family = {'parents': parents, 'children': children}
        return a_family

    def family_member(self, sex):
        info = ['name', 'sex', 'birthdate', 'blood group', 'mail']
        family_member = fake.profile(fields=info, sex=sex)
        name_array = family_member['name'].split()
        if len(name_array) > 2:
            name_array.pop(0)
            family_member['name'] = ' '.join(name_array)
        family_member['birthdate'] = datetime.strptime(
            family_member['birthdate'],
            "%Y-%m-%d")
        return family_member


fake.add_provider(FamilyProvider)
