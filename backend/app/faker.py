from faker import Factory
from faker.providers import BaseProvider

fake = Factory.create('en_GB')


class FamilyProvider(BaseProvider):
    ''' A family and family member Faker provider '''

    def family(self, size, inject=None):
        parents = [
            self.family_member(sex='Male'),
            self.family_member(sex='Female')
        ]
        children = []
        for _ in range(0, size - 2):
            a_child = self.family_member(
                sex=fake.random.choice(['Male', 'Female']))
            children.append(a_child)

        # replace inject type relative with inject member
        # if inject object is provided.
        # where inject = {
        #       'type': ['parent','child'],
        #       'member': family_member
        # }
        if inject:
            if inject['type'] == 'parent':
                parents[0] = inject['member']
            elif inject['type'] == 'child':
                children[0] = inject['member']
        return {'parents': parents, 'children': children}

    def family_member(self, email=None, sex='Male'):
        family_member = {}
        if sex == 'Male':
            family_member = {
                'first_name': fake.first_name_male(),
                'ethnic_name': fake.first_name_male(),
                'last_name': fake.last_name_male(),
                'sex': 'Male',
                'birth_date': fake.past_date(),
                'email': email or fake.safe_email()
            }
        elif sex == 'Female':
            family_member = {
                'first_name': fake.first_name_female(),
                'ethnic_name': fake.first_name_female(),
                'last_name': fake.last_name_female(),
                'sex': 'Female',
                'birth_date': fake.past_date(),
                'email': email or fake.safe_email()
            }
        return family_member


fake.add_provider(FamilyProvider)
