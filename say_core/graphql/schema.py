import graphene
from django.conf import settings
from graphene_django.debug import DjangoDebug

from say_core.users.schema import Mutation as UsersMutation
from say_core.users.schema import Query as UsersQuery


class Query(UsersQuery, graphene.ObjectType):
    if settings.PLUGGABLE_FUNCS.DEBUG_TOOLBAR:
        debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(graphene.ObjectType, UsersMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
