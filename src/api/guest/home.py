from src.api.public.main import *

@auth_guest
def index(request, usr):
    return response(status=True)
