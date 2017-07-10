from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


class Relations:
    '''A model of weighted relations and labels'''

    all_types = {
        1: 'Partner', 2: 'Sibling', 3: 'Parent',
        4: 'Child', 5: 'Niece-Nephew', 6: 'Uncle-Aunt'
    }
    undirected_types = [1, 2]
    directed_types = [3, 4]
    modifiers = ['Great', 'Grand', 'In-law']

    @staticmethod
    def get_inverse_weight(weight):
        weight_pairings = [
            {1: 1},
            {2: 2},
            {3: 4},
            {4: 3}
        ]
        for pair in weight_pairings:
            for key, value in pair.items():
                if key == weight:
                    return value
        return None


def get_one_or_create(session,
                      model,
                      create_method='',
                      create_method_kwargs=None,
                      **kwargs):
    # reference: http://skien.cc/blog/2014/01/15/
    # sqlalchemy-and-race-conditions-implementing/
    try:
        return session.query(model).filter_by(**kwargs).one(), True
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, False
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), True
