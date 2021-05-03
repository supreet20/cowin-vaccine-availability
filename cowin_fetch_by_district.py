import requests
import datetime
import json
import pandas as pd

flag_response = input("Do you want to enter data (y/n):")
city_flag = 'n'

if(flag_response.lower() == 'y' or  flag_response.lower()=="yes"):   
    state_response = input("Please Enter State for which you want data:")
    weeks_response = int(input("Please Enter number of weeks for which you want data:"))
    age_response = int(input("Please Enter your age:"))
    city_flag = input("Do you want city/district specific data (y/n):")
    if(city_flag.lower() == 'y' or  city_flag.lower()=="yes"): 
        city_response = input("Please Enter district for which you want data:")

else:
    state_response = "Delhi"
    weeks_response = 2
    age_response = 25
    city_response = "North Delhi"
#141      Central Delhi
#145      East Delhi
#140      New Delhi
#146      North Delhi
#147      North East Delhi
#143      North West Delhi
#148      Shahdara
#149      South Delhi
#144      South East Delhi
#150      South West Delhi
#142      West Delhi

response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states")
json_data = json.loads(response.text)

state_check_flag = 0

for state_data in json_data['states']:
    if(state_data['state_name'].lower() == state_response.lower()):
        print(state_data['state_id'], '\t', state_data['state_name'])
        state_check_flag = 1
        final_state_code = state_data['state_id']
        final_state_name = state_data['state_name']
        break
    else:
        continue

if(state_check_flag==0):
    print("Please enter valid state")

#final_state_code = 9 #Delhi

print("State code: ", final_state_code)
print("State Name: ", final_state_name)

district_ids = []
city_id =[]

response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(final_state_code))
json_data = json.loads(response.text)
for district_data in json_data["districts"]:
   print(district_data["district_id"],'\t', district_data["district_name"])
   district_ids.append(district_data["district_id"])
   if(city_flag.lower() == 'y' or  city_flag.lower()=="yes"):
       if(district_data['district_name'].lower() == city_response.lower()):
           city_id.append(district_data["district_id"])

print("\n")

if(city_flag.lower() == 'y' or city_flag.lower()=="yes"): 
    district_ids= city_id

numdays = int(weeks_response)
age = age_response

# Print details flag
print_flag = 'Y'

date_today_base = datetime.datetime.today()
date_list = [date_today_base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

dataframe = []
final_data_frame = []

for input_date in date_str:
    for district_id in district_ids:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(district_id, input_date)
        response = requests.get(URL)
        if response.ok:
            resp_json = response.json()
            if resp_json["centers"]:
                  if(print_flag=='y' or print_flag=='Y'):
                      for centre in resp_json["centers"]:
                         for session in centre['sessions']:
                            dataframe=[]
                            dataframe2=[]
                            if ((session["min_age_limit"] <= age) and (session["available_capacity"] > 0)):
                                dataframe.append(session['date'])
                                dataframe.append(centre["name"])
                                dataframe.append(centre["district_name"])
                                dataframe.append(centre["state_name"])
                                dataframe.append(centre["fee_type"])
                                dataframe.append(session["available_capacity"])
                                dataframe.append(session["vaccine"])
                                dataframe.append(centre["pincode"])
                                dataframe.append(session['min_age_limit'])
                                dataframe2.append(session['slots'])
                                dataframe.append(dataframe2)
                                final_data_frame.append(dataframe)


pd.set_option('display.max_rows', None)                           
df = pd.DataFrame(final_data_frame, columns = ['Date', 'Name','District Name',
'State Name','Fee Type','Available Capacity', 'Vaccine', 'Pin Code','Age Limit', 'Slots'])
print(df)

#render dataframe as html
html = df.to_html()

#write html to file
text_file = open("index.html", "w")
text_file.write(html)
text_file.close()