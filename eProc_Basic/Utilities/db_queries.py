# from eProc_Login.models import UserData


# To get client details for logged in user
def getClients(request):
    client = request.user.client
    return client

def getUsername(request):
    username = request.user.username
    return username