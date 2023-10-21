from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import REST_AUTH


@api_view()
def root_route(request):
    return Response({
        "message": "This is The APi of PP55"
    })


# dj-rest-auth logout view fix
@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key='my-app-auth',
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite='None',
        secure=True,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite='None',
        secure=True,
    )
    return response