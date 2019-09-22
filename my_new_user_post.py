from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import my_user_album

@route("/albums/<artist>")
def albums(artist):
    albums_list = my_user_album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [my_user_album.album for my_user_album in albums_list]
        result = "Список альбомов {}:<hr>".format(artist)
        result += "<li></li>".join(album_names)
    return result


@route("/albums", method="POST")
def create_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Проверьте правильность написания года")

    try:
        new_album = my_user_album.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except my_user_album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:    
#        print("New album № {} saved".format(new_album.id))
        result = "Альбом № {} сохранен".format(new_album.id)
    return result
    

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)