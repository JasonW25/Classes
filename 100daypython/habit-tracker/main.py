import requests
import datetime as dt

today = dt.datetime.now()
headers = {
    "X-USER-TOKEN": ""
}


# post pixel

# pixela_endpoint = "https://pixe.la/v1/users/jasontwebb-250/graphs/graph1"
# user_params = {
#     "date": today.strftime("%Y%m%d"),
#     "quantity": "5"
# }

# response = requests.post(url=pixela_endpoint, json=user_params, headers=headers)


#update pixel

# date = "20220102"
# pixela_endpoint = f"https://pixe.la/v1/users/jasontwebb-250/graphs/graph1/{date}"
# user_params = {
#     "quantity": "8"
# }

# response = requests.put(url=pixela_endpoint, json=user_params, headers=headers)


# delete pixel

date = "20220102"
pixela_endpoint = f"https://pixe.la/v1/users/jasontwebb-250/graphs/graph1/{date}"

response = requests.delete(url=pixela_endpoint, headers=headers)

print(response.text)
