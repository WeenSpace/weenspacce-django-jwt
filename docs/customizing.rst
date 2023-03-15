Customizing
===========

If you want to customize the ``Create`` behavior, you'll need to customize the ``resolve()`` method on a subclass of:

  .. autoclass:: django_jwt.JWTMutation

::

    import graphene
    import django_jwt


    class Create(django_jwt.JWTMutation):
        user = graphene.Field(UserType)

        @classmethod
        def resolve(cls, root, info, **kwargs):
            return cls(user=info.context.user)

Authenticate the user and obtain a **JSON Web Token** and the *user id*::

    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
        user {
          id
        }
      }
    }
