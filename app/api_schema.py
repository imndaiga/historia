from graphene import ObjectType, Schema, List
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Person as PersonModel
from .models import Link as LinkModel


class Person(SQLAlchemyObjectType):
    class Meta:
        model = PersonModel


class Link(SQLAlchemyObjectType):
    class Meta:
        model = LinkModel


class Query(ObjectType):
    all_persons = List(Person)
    all_edges = List(Link)

    def resolve_all_Persons(self, args, context, info):
        query = Person.get_query(context)
        return query.all()

    def resolve_all_edges(self, args, context, info):
        query = Link.get_query(context)
        return query.all()


schema = Schema(query=Query)
