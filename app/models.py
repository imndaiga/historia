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

	def create_step_edge(self, node, edge_weight):
		if self.baptism_name != node.baptism_name:
			if node.yob > self.yob:
				if not self._is_step_ascendant_to(node):
					n = Edge(ascendant=self, descendant=node, edge_weight=edge_weight)
					db.session.add(n)
					return self
			else:
				if not node._is_step_ascendant_to(self):
					n = Edge(ascendant=node, descendant=self, edge_weight=edge_weight)
					db.session.add(n)
					return node
		return False

	def change_step_edge_weight(self, node, edge_weight):
		if self.baptism_name != node.baptism_name:
			if self._is_step_ascendant_to(node):
				n = Edge.query.filter_by(descendant_id=node.id).first()
			elif self._is_step_descendant_to(node):
				n = Edge.query.filter_by(ascendant_id=node.id).first()
			else:
				# Self and Node are not related, no edge_weight change can be made
				return False
			n.edge_weight = edge_weight
			db.session.add(n)
			return True
		return False

	@staticmethod
	def commit_node_branch(links=None):
		if links:
			for link in links:
				db.session.add_all([links[link][0],links[link][1]])
				db.session.commit()
				links[link][0].create_step_edge(links[link][1], edge_weight=links[link][2])
			return True
		else:
			return False

	def count_steps(self, node):
		pass

	def _is_step_ascendant_to(self, node):
		return self.descended_by.filter_by(
			descendant_id=node.id).first() is not None

	def _is_step_descendant_to(self, node):
		return self.ascended_by.filter_by(
			ascendant_id=node.id).first() is not None
					
	def __repr__(self):
		return 'Node: <%s>' % self.baptism_name