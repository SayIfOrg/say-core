import graphql_jwt

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .filters import UserFilter
from .models import User


class JWTMutation:
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)
        fields = ("id", "username", "name")

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class Query(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserType)
    users = DjangoFilterConnectionField(UserType, filterset_class=UserFilter)


class Mutation(JWTMutation):
    pass
