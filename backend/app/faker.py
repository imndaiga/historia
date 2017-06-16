from faker import Factory
from faker.providers import BaseProvider

fake = Factory.create('en_GB')


class FamilyProvider(BaseProvider):
    def family(self, seed, size, injection=[]):
        fake.seed(seed)
        if len(injection) == 0:
            parents = [self.family_member(sex='Male'),
                       self.family_member(sex='Female')]
            children = []
            for _ in range(0, size - 2):
                a_child = self.family_member(
                    sex=fake.random.choice(['Male', 'Female']))
                children.append(a_child)
        else:
            if injection[0] == 'parents':
                parents = [self.family_member(sex='Male'),
                           self.family_member(sex='Female')]
                children = [injection[1]]
                for _ in range(0, size - 3):
                    a_child = self.family_member(
                        sex=fake.random.choice(['Male', 'Female']))
                    children.append(a_child)
            else:
                if injection[1]['sex'] == 'Male':
                    parents = [injection[1],
                               self.family_member(sex='Female')]
                else:
                    parents = [injection[1],
                               self.family_member(sex='Male')]
                children = []
                for _ in range(0, size - 2):
                    a_child = self.family_member(
                        sex=fake.random.choice(['Male', 'Female']))
                    children.append(a_child)
        a_family = {'parents': parents, 'children': children}
        return a_family

    def family_member(self, sex='Male'):
        if sex == 'Male':
            family_member = {
                'first_name': fake.first_name_male(),
                'ethnic_name': fake.first_name_male(),
                'last_name': fake.last_name_male(),
                'sex': 'Male',
                'birth_date': fake.past_date(),
                'email': fake.safe_email()
            }
        elif sex == 'Female':
            family_member = {
                'first_name': fake.first_name_female(),
                'ethnic_name': fake.first_name_female(),
                'last_name': fake.last_name_female(),
                'sex': 'Female',
                'birth_date': fake.past_date(),
                'email': fake.safe_email()
            }
        return family_member


fake.add_provider(FamilyProvider)
