from graphene import ObjectType, Schema, List
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Node as NodeModel
from .models import GlobalEdge as GlobalEdgeModel


class Node(SQLAlchemyObjectType):
    class Meta:
        model = NodeModel


class GlobalEdge(SQLAlchemyObjectType):
    class Meta:
        model = GlobalEdgeModel


class Query(ObjectType):
    all_nodes = List(Node)
    all_edges = List(GlobalEdge)

    def resolve_all_nodes(self, args, context, info):
        query = Node.get_query(context)
        return query.all()

    def resolve_all_edges(self, args, context, info):
        query = GlobalEdge.get_query(context)
        return query.all()


schema = Schema(query=Query)
