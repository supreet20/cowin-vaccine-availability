# cowin-vaccine-availability

This python script fetches the covid vaccination centres(cowin portal) based on :
 - Age
 - State
 - Number of weeks for appointment
 - City (Soon)

## Steps to run

Make sure python(>3.7) is intalled on your device

 - Install requests and pandas module in your system

 Requests Module
 For mac : pip install requests
 Fow windows : python -m pip install requests

 Pandas Module
 For mac : pip install pandas
 Fow windows : python -m pip install pandas

 - Run the python file
'''
python cowin_fetch_by_district.py
''''

 - Open the index.html file where you cloned the repo and voila, you have the list.

## Few tips 

 - If you want to skip entering data eveyrtime when the code asks : 
 "Do you want to enter data (y/n):", you can do so by doing the following changes in code
 In the cowin_fetch_by_district
 Change the lines 17,18,19,20 as :
 state_response = "Your_state" (eg. "Delhi")
 weeks_response = Num_Of_weeks (eg. 2)
 age_response = Your_age(For eg. 25)
 city_response = "Your_district" (For eg. "North Delhi", "BBMP", "Bangalore Urban" etc)