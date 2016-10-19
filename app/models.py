from . import db
from datetime import date

class Edge(db.Model):
	"""self-referential association table that connects Nodes"""
	__tablename__ = 'Edges'
	ascendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
		primary_key=True)
	descendant_id = db.Column(db.Integer, db.ForeignKey('nodes.id'),
		primary_key=True)
	edge_weight = db.Column(db.Integer)

	def __repr__(self):
		return '<Edge %s-%s:%s>' % (self.ascendant_id, self.descendant_id, self.edge_weight)

class Node(db.Model):
	"""all miminani subscribed Nodes"""
	__tablename__ = 'nodes'
	id = db.Column(db.Integer, primary_key=True)
	baptism_name = db.Column(db.String(64))
	ethnic_name = db.Column(db.String(64), index=True)
	surname = db.Column(db.String(64), index=True)
	sex = db.Column(db.String(64))
	yob = db.Column(db.DateTime, default=date(9999,1,1))
	email_confirmed = db.Column(db.Boolean, default=False)
	email = db.Column(db.String(64), unique=True)

	descended_by = db.relationship('Edge',
								foreign_keys=[Edge.ascendant_id],
								backref=db.backref('ascendant', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')
	ascended_by = db.relationship('Edge',
								foreign_keys=[Edge.descendant_id],
								backref=db.backref('descendant', lazy='joined'),
								lazy='dynamic',
								cascade='all, delete-orphan')

	def step_ascend(self, node, relation):
		if not self.is_step_ascendant_to(node):
			n = Edge(ascendant=self, descendant=Node, relation=relation)
			db.session.add(n)

	def step_descend(self, node, relation):
		if not self.is_step_descendant_to(node):
			n = Edge(ascendant=Node, descendant=self, relation=relation)
			db.session.add(n)

	def is_step_ascendant_to(self, node):
		return self.descended_by.filter_by(
			descendant_id=node.id).first() is not None

	def is_step_descendant_to(self, node):
		return self.ascended_by.filter_by(
			ascendant_id=node.id).first() is not None

	def change_step_relation(self, node, relation):
		if self.is_step_ascendant_to(node):
			n = Edge.query.filter_by(descendant_id=node.id).first()
		elif self.is_step_descendant_to(node):
			n = Edge.query.filter_by(ascendant_id=node.id).first()
		else:
			# Self and Node are not related, no relation change can be made
			return False
		n.relation = relation
		db.session.add(n)
		return True

	def switch_step_hierarchy(self,node):
		if self.is_step_ascendant_to(node):
			n = Edge.query.filter_by(descendant_id=node.id).first()
			n.descendant_id = self.id
			n.ascendant_id = node.id
		elif self.is_step_descendant_to(node):
			n = Edge.query.filter_by(ascendant_id=node.id).first()
			n.ascendant_id = self.id
			n.descendant_id = node.id
		else:
			# Self and Node are not related, no relation change can be made
			return False
		db.session.add(n)
		return True

	def count_steps(self, node):
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
			for node in nuclei[key]:
				node_is_master = Node.query.filter_by(baptism_name=node).first()
				if not node_is_master:
					nucleic_family.append(Node(baptism_name=node))
				else:
					master_found = node_is_master
			db.session.add_all(nucleic_family)
			db.session.commit()

			if not master_found:
				for index,node in enumerate(nucleic_family):
					if index==0:
						n1 = Edge(ascendant=node,descendant=nucleic_family[index+1],edge_weight=0)
						n2 = Edge(ascendant=node,descendant=nucleic_family[index+2],edge_weight=1)
						n3 = Edge(ascendant=node,descendant=nucleic_family[index+3],edge_weight=1)
					if index==1:
						n4 = Edge(ascendant=node,descendant=nucleic_family[index+1],edge_weight=1)
						n5 = Edge(ascendant=node,descendant=nucleic_family[index+2],edge_weight=1)
					if index==2:
						n6 = Edge(ascendant=node,descendant=nucleic_family[index+1],edge_weight=0)
			else:
				for index,node in enumerate(nucleic_family):
					if index==0:
						n1 = Edge(ascendant=master_found,descendant=nucleic_family[index],edge_weight=0)
						n2 = Edge(ascendant=master_found,descendant=nucleic_family[index+1],edge_weight=1)
						n3 = Edge(ascendant=master_found,descendant=nucleic_family[index+2],edge_weight=1)
						n4 = Edge(ascendant=node,descendant=nucleic_family[index+1],edge_weight=1)
						n5 = Edge(ascendant=node,descendant=nucleic_family[index+2],edge_weight=1)
					if index==1:
						n6 = Edge(ascendant=node,descendant=nucleic_family[index+1],edge_weight=0)
				master_found = None
			db.session.add_all([n1,n2,n3,n4,n5,n6])		
			db.session.commit()



	def __repr__(self):
		return 'Node: <%s>' % self.baptism_name