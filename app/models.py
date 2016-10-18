from . import db
from datetime import date

class Node(db.Model):
	"""self-referential association table that connects persons"""
	__tablename__ = 'nodes'
	ascendant_id = db.Column(db.Integer, db.ForeignKey('persons.id'),
		primary_key=True)
	descendant_id = db.Column(db.Integer, db.ForeignKey('persons.id'),
		primary_key=True)
	edge_weight = db.Column(db.Integer)

	def __repr__(self):
		return '<Node %s-%s:%s>' % (self.ascendant_id, self.descendant_id, self.edge_weight)

class Person(db.Model):
	"""all miminani subscribed persons"""
	__tablename__ = 'persons'
	id = db.Column(db.Integer, primary_key=True)
	baptism_name = db.Column(db.String(64))
	ethnic_name = db.Column(db.String(64), index=True)
	surname = db.Column(db.String(64), index=True)
	sex = db.Column(db.String(64))
	yob = db.Column(db.DateTime, default=date(9999,1,1))
	email_confirmed = db.Column(db.Boolean, default=False)
	email = db.Column(db.String(64), unique=True)

	descended_by = db.relationship('Node',
								foreign_keys=[Node.ascendant_id],
								backref=db.backref('ascendant', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')
	ascended_by = db.relationship('Node',
								foreign_keys=[Node.descendant_id],
								backref=db.backref('descendant', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')

	def step_ascend(self, person, relation):
		if not self.is_step_ascendant_to(person):
			n = Node(ascendant=self, descendant=person, relation=relation)
			db.session.add(n)

	def step_descend(self, person, relation):
		if not self.is_step_descendant_to(person):
			n = Node(ascendant=person, descendant=self, relation=relation)
			db.session.add(n)

	def is_step_ascendant_to(self, person):
		return self.descended_by.filter_by(
			descendant_id=person.id).first() is not None

	def is_step_descendant_to(self, person):
		return self.ascended_by.filter_by(
			ascendant_id=person.id).first() is not None

	def change_step_relation(self, person, relation):
		if self.is_step_ascendant_to(person):
			n = Node.query.filter_by(descendant_id=person.id).first()
		elif self.is_step_descendant_to(person):
			n = Node.query.filter_by(ascendant_id=person.id).first()
		else:
			# Self and person are not related, no relation change can be made
			return False
		n.relation = relation
		db.session.add(n)
		return True

	def switch_step_hierarchy(self,person):
		if self.is_step_ascendant_to(person):
			n = Node.query.filter_by(descendant_id=person.id).first()
			n.descendant_id = self.id
			n.ascendant_id = person.id
		elif self.is_step_descendant_to(person):
			n = Node.query.filter_by(ascendant_id=person.id).first()
			n.ascendant_id = self.id
			n.descendant_id = person.id
		else:
			# Self and person are not related, no relation change can be made
			return False
		db.session.add(n)
		return True

	def count_steps(self, person):
		pass

	@staticmethod
	def commit_test_tree():
		nuclei = {
				1 : ['John','Mary', 'Jack', 'Mark'],
				2 : ['Jack', 'Lucy', 'Ben', 'Lynda'],
				3 : ['Mark', 'Anne', 'Michael', 'Janet'],
				4 : ['Ben', 'Ruth', 'Susan', 'Beth'],
				5 : ['Beth', 'Andrew', 'Cyrus','Lloyd'],
				6 : ['Michael', 'Lucille', 'Anthony', 'Lucas'],
				7 : ['Janet', 'Moses', 'Joy', 'Edgar'],
				8 : ['Lucas', 'Marjorie', 'Margot', 'Alan'],
				9 : ['Alan', 'Sarah', 'Daniel', 'Ginette'],
				10 : ['Daniel', 'Loise', 'Clark', 'Henry']
		}
		master_found = None
		for key in nuclei:
			nucleic_family = []
			for person in nuclei[key]:
				person_is_master = Person.query.filter_by(baptism_name=person).first()
				if not person_is_master:
					nucleic_family.append(Person(baptism_name=person))
				else:
					master_found = person_is_master
			db.session.add_all(nucleic_family)
			db.session.commit()

			if not master_found:
				for index,person in enumerate(nucleic_family):
					if index==0:
						n1 = Node(ascendant=person,descendant=nucleic_family[index+1],edge_weight=0)
						n2 = Node(ascendant=person,descendant=nucleic_family[index+2],edge_weight=1)
						n3 = Node(ascendant=person,descendant=nucleic_family[index+3],edge_weight=1)
					if index==1:
						n4 = Node(ascendant=person,descendant=nucleic_family[index+1],edge_weight=1)
						n5 = Node(ascendant=person,descendant=nucleic_family[index+2],edge_weight=1)
					if index==2:
						n6 = Node(ascendant=person,descendant=nucleic_family[index+1],edge_weight=0)
			else:
				for index,person in enumerate(nucleic_family):
					if index==0:
						n1 = Node(ascendant=master_found,descendant=nucleic_family[index],edge_weight=0)
						n2 = Node(ascendant=master_found,descendant=nucleic_family[index+1],edge_weight=1)
						n3 = Node(ascendant=master_found,descendant=nucleic_family[index+2],edge_weight=1)
						n4 = Node(ascendant=person,descendant=nucleic_family[index+1],edge_weight=1)
						n5 = Node(ascendant=person,descendant=nucleic_family[index+2],edge_weight=1)
					if index==1:
						n6 = Node(ascendant=person,descendant=nucleic_family[index+1],edge_weight=0)
				master_found = None
			db.session.add_all([n1,n2,n3,n4,n5,n6])		
			db.session.commit()

		return 'Test tree committed to database'



	def __repr__(self):
		return 'Person: <%s>' % self.baptism_name