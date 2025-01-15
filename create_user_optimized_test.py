import sender_stand_request
import data


# esta función cambia los valores en el parámetro "firstName"
def get_user_body(first_name):
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body


# Función de prueba positiva
def positive_assert(first_name):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(first_name)
    # El resultado de la solicitud para crear un/a nuevo/a usuario/a se guarda en la variable user_response
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""

    # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
    users_table_response = sender_stand_request.get_users_table()

    # String que debe estar en el cuerpo de respuesta
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    user_body_neg = get_user_body(first_name)
    # Comprueba si esta función recibe una versión actualizada del cuerpo de solicitud de creación de un nuevo usuario o usuaria a la variable user_body.
    response = sender_stand_request.post_new_user(user_body_neg)
    # Comprueba si la respuesta contiene el código 400.
    assert response.status_code == 400
    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400.
    assert response.json()["code"] == 400
    # Comprueba si el atributo "message" en el cuerpo de la respuesta se ve así: "Nombre de usuario o usuaria incorrecto. El nombre solo puede contener letras latinas y la longitud debe ser de 2 a 15 caracteres".
    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. El nombre solo puede contener letras del alfabeto latino, la longitud debe ser de 2 a 15 caracteres."
   # assert response.json()["message"] == "El nombre que ingresaste es incorrecto. " \
   #                                      "Los nombres solo pueden contener caracteres latinos,  "\
    #                                     "los nombres deben tener al menos 2 caracteres y no más de 15 caracteres"

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    # Comprueba si la respuesta contiene el código 400.
    assert response.status_code == 400
    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400.
    assert response.json()["code"] == 400
    #Comprueba si el atributo "message" en el cuerpo de respuesta se ve así: "No se enviaron todos los parámetros necesarios".
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"
    #assert response.json()["message"] == "No se enviaron todos los parámetros necesarios"
 
# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("AV")
# Prueba 2. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("AndreaVelascoGa")
# Prueba 3. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene simbolos caracteres
def test_create_user_symbols_in_first_name_get_error_response():
    negative_assert_symbol("Andr#a")

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("AndreaVelascoGar")

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A aa")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("Andrea1")

def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

# Prueba 9. Error
# El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body("")
    # Comprueba la respuesta
    negative_assert_no_first_name(user_body)

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    negative_assert_symbol(user_body)
