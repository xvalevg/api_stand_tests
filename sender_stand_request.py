import configuration
import data
import requests


def get_docs():
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)


def get_logs():
    params ={"count":20}
    return requests.get(configuration.URL_SERVICE + configuration.LOG_MAIN_PATH , params)

def get_users_table():
     return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH )    

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # inserta la dirección URL completa
                         json=body,  # inserta el cuerpo de solicitud
                         headers=data.headers)  # inserta los encabezados
def post_products_kits(productIds):
    return requests.post(configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,  # inserta la dirección URL completa
                         json=productIds,  # inserta el cuerpo de solicitud
                         headers=data.headers)  # inserta los encabezados

# response = get_docs()
# print(response.status_code)

# logs_response = get_logs()
# print (logs_response.headers)

# data_response = get_users_table()
# print (data_response.status_code)

#response = post_new_user(data.user_body)
#print(response.json())

productsResponse = post_products_kits(data.product_ids)
print(productsResponse.status_code)
print(productsResponse.json())

