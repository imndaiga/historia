from graphene import ObjectType, Schema, List
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Node as NodeModel
from .models import Edge as EdgeModel

class Node(SQLAlchemyObjectType):
	class Meta:
		model = NodeModel

class Edge(SQLAlchemyObjectType):
	class Meta:
		model = EdgeModel

class Query(ObjectType):
	all_nodes = List(Node)
	all_edges = List(Edge)

	def resolve_all_nodes(self, args, context, info):
		query = Node.get_query(context)
		return query.all()

	def resolve_all_edges(self, args, context, info):
		query = Edge.get_query(context)
		return query.all()

schema = Schema(query=Query)