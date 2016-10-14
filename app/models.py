from . import db
from datetime import date

class Node(db.Model):
	"""self-referential association table that connects persons"""
	__tablename__ = 'nodes'
	ascendant_id = db.Column(db.Integer, db.ForeignKey('persons.id'),
		primary_key=True)
	descendant_id = db.Column(db.Integer, db.ForeignKey('persons.id'),
		primary_key=True)
	relation = db.Column(db.String(20))

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

	def count_hierarchy_steps(self, person):
		pass

	def __repr__(self):
		return 'Person: <%s>' % self.baptism_name