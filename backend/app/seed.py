from flask_script import Command, Option
import os
from .faker import fake


class Seed(Command):
    """Create fake seed data and store in database"""

    option_list = (
        Option('--units', '-u', dest='units'),
        Option('--size', '-s', dest='size'),
        Option('--layers', '-l', dest='layers', default=0),
        Option('--verbose', '-v', dest='verbose', action='store_true')
    )

    def init_app(self, app):
        from app.models import Person, Link, get_one_or_create
        from app import db, graph
        self.Person = Person
        self.Link = Link
        self.db = db
        self.graph = graph
        self.get_one_or_create = get_one_or_create
        fake.seed(4321)

    def run(self, units, size, layers, verbose=False):
        self.verbose = verbose

        unchecked_dict_families = []
        filtered_person_families = []
        relationships = []

        # create [units] distinct family trees.
        for _ in range(units):
            unchecked_dict_families.extend(self.get_family_tree(size, layers))

        filtered_person_families = self.save_persons_to_db(
            unchecked_dict_families
        )
        relationships = self.save_relationships_to_db(filtered_person_families)
        self.graph.update()

        return filtered_person_families, relationships

    def get_family_tree(self, size, layers):
        store = []
        queue = []
        tree = []

        first_family = fake.family(size=size)
        if os.environ.get('HISTORIA_ADMIN'):
            first_family['parents'][0] = fake.family_member(
                email=os.environ.get('HISTORIA_ADMIN')
            )
        store.append(first_family)

        for _ in range(layers + 1):
            queue = store[:]
            store = []
            for family in queue:
                if self.count_family_member_instances(family, tree) < 2:
                    tree.append(family)
                    store.extend(self.add_layer(family, size))

        return tree

    def add_layer(self, family, size):
        next_layer = []

        for relation, inject_type in {
            'children': 'parent', 'parents': 'child'
        }.items():
            # get family members who belong to the
            # current operation's relation.
            members = [
                l[i] for k, l in family.items()
                for i in range(len(l))
                if k == relation
            ]
            # for each member, create an opposite relation family.
            # i.e. if current member has a parent relation,
            # create a new family where member is a child
            # and vice versa.
            for member in members:
                next_layer.append(fake.family(
                    size=size,
                    inject={
                        'type': inject_type,
                        'member': member
                    }
                ))

        return next_layer

    def save_persons_to_db(self, list_of_families):
        # reference list_of_families from person_list_of_families
        # copying would be a waste of memory.
        person_list_of_families = list_of_families
        for f_index, family in enumerate(person_list_of_families):
            for relation in family:
                for m_index, member in enumerate(family[relation]):
                    person, exists = self.get_one_or_create(
                        session=self.db.session,
                        model=self.Person,
                        create_method='create_from_email',
                        create_method_kwargs={
                            'first_name': member['first_name'],
                            'ethnic_name': member['ethnic_name'],
                            'last_name': member['last_name'],
                            'sex': member['sex'],
                            'birth_date': member['birth_date']
                        },
                        email=member['email']
                    )
                    # Perform a callback if user exists?

                    # replace family members in list_of_families
                    # with person models.
                    person_list_of_families[
                        f_index][relation][m_index] = person
        self.db.session.commit()

        return person_list_of_families

    def save_relationships_to_db(self, person_list_of_families):
        relationship_list = []
        for family in person_list_of_families:
            for relation in family:
                for index, member in enumerate(family[relation]):
                    if relation == 'parents':
                        # create parent to child relationships.
                        for child in family['children']:
                            relationship, exists = \
                                member.get_or_create_relation(
                                    child, 3)
                            # do some stuff if an error occured.
                            if not exists:
                                relationship_list.append(relationship)

                        # create partner to partner relationships.
                        for partner_index in range(len(family['parents'])):
                            if index != partner_index:
                                partner = family[relation][partner_index]
                                relationship, exists = \
                                    member.get_or_create_relation(
                                        partner, 1)
                                if not exists:
                                    relationship_list.append(relationship)

                    # create child to parent relationships.
                    elif relation == 'children':
                        for parent in family['parents']:
                            relationship, exists = \
                                member.get_or_create_relation(
                                    parent, 4)
                            # do some stuff if an error occured.
                            if not exists:
                                relationship_list.append(relationship)

                        # create sibling to sibling relationships.
                        for sibling_index in range(len(family['children'])):
                            if index != sibling_index:
                                sibling = family[relation][sibling_index]
                                relationship, exists = \
                                    member.get_or_create_relation(
                                        sibling, 2)
                                if not exists:
                                    relationship_list.append(relationship)

        self.db.session.commit()

        return relationship_list

    @staticmethod
    def count_family_member_instances(family_dict, list_of_families):
        duplication_count = 0
        for fd in list_of_families:
            for relation1 in fd:
                for relation2 in family_dict:
                    for member1 in fd[relation1]:
                        for member2 in family_dict[relation2]:
                            if member2 == member1:
                                duplication_count += 1

        return duplication_count
