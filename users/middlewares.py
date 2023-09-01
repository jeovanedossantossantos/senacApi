from django.conf import settings
import jwt

class Middlewares():

    def decode(tokem):
        print("teste")
        print(tokem.get('token'))
        print("teste")
        if("Bearer" in tokem.get('token')):
            des = jwt.decode(tokem.get('token').split(' ')[1],settings.SECRET_KEY, algorithms=['HS256'])
        else:
            des = jwt.decode(tokem.get('token'),settings.SECRET_KEY, algorithms=['HS256'])

        return des["user_id"]