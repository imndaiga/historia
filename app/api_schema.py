import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from .models import Node as NodeModel
from .models import Edge as EdgeModel

class Node(SQLAlchemyObjectType):
	class Meta:
		model = NodeModel

class Edge(SQLAlchemyObjectType):
	class Meta:
		model = EdgeModel

class Query(graphene.ObjectType):
	nodes = graphene.List(Node)
	edges = graphene.List(Edge)

	def resolve_nodes(self, args, context, info):
		query = Node.get_query(context)
		return query.all()

	def resolve_edges(self, args, context, info):
		query = Edge.get_query(context)
		return query.all()

schema = graphene.Schema(query=Query)