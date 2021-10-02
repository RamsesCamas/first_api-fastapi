import json
import requests

URL = 'http://localhost:8000/api/v1/reviews'
HEADERS = {'accept':'application/json'}
QUERYSET = {'page':2,'limit':1}
REVIEW = {
            'user_id':4,
            'movie_id':1,
            'review':'Me encantó la película',
            'score':87
            }

def get_method():
    response = requests.get(URL,headers=HEADERS)
    if response.status_code == 200 and response.headers.get('content-type') == 'application/json':
        reviews = response.json()
        for review in reviews:
            print(review.get('movie').get('title') + ' - ' + str(review.get('score')))

def post_method():
    response = requests.post(URL,json=REVIEW)
    if response.status_code == 200:
        print('Reseña creada')
        #print(response.json()['id'])
    else:
        print(response.content)

def put_method():
    review_id = 3
    review = {
        'review':'Ya me gustó la pelicula',
        'score': 75
    }
    url = URL + f'/{review_id}'
    response = requests.put(url,json=review)
    if response.status_code == 200:
        print('La reseña se actualizó correctamente')
        print(response.json())

def delete_method():
    review_id = 2
    url = URL + f'/{review_id}'
    response = requests.delete(url)
    if response.status_code == 200:
        print('La reseña se eliminó correctamente')
        print(response.json())

def login_method():
    url = 'http://localhost:8000/api/v1/users'
    USER ={
        'username':'ramses_client',
        'password':'123456'
    }
    response = requests.post(url+'/login',json=USER)
    if response.status_code == 200:
        my_cookie  = response.cookies.get_dict()
        new_response = requests.get(url+'/reviews',cookies=my_cookie)
        if new_response.status_code == 200:
            for review in new_response.json():
                print(f"{review['review']} - {review['score']}")

if __name__ == '__main__':
    #post_method()
    #put_method()
    #delete_method()
    #get_method()
    login_method()