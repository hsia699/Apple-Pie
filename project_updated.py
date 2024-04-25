# -*- coding: utf-8 -*-
"""
Team: Apple Pie
Member Names: Ash Wang, Jingxia Zhong, Nana Oye Djan, Seung Gyu Baik, Yi Ren
Andrew IDs: congleiw, jingxiaz, ndjan, seunggyb, yren2
"""

#%%Setup and Loading Data
import pandas as pd
import numpy as np
import fredpy as fp
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import calendar
import matplotlib.pyplot as plt

#CSV data source
airfare_data = pd.read_csv('Airfare Data.csv', sep = ',')

#Web scraped data source
# The website we need to scrap
url = 'https://www.usinflationcalculator.com/inflation/airfare-inflation/'

# Send HTTP request to the URL
response = requests.get(url)

# Make sure the request was successful
if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all divs with the specified style
    divs = soup.find_all('div', style='overflow-x:auto;')
    
    # Check if we found any divs and select the first table within the first div
    if divs:
        # The target table is the first table below the first div
        table = divs[0].find('table')
        # Convert the table to a DataFrame
        airfare_inflation = pd.read_html(str(table), header = 0, index_col = 0)[0]
        airfare_inflation = airfare_inflation.apply(pd.to_numeric, errors = 'coerce')
        # Save the DataFrame to an Excel file as backup
        excel_path = 'airfare_inflation_data.xlsx'
        airfare_inflation.to_excel(excel_path, index=False)
        print(f"Data successfully saved to {excel_path}")
    else:
        print('Table not found.')
else:
    print('Failed to scrap the webpage')
    
#API Data Source
fp.api_key = 'ccb3e5950162f6c94456a50f29acd3f1'

# Specify the API path
path = 'fred/series/observations'

# Set observation_date string as today's date
observation_date = datetime.today().strftime('%Y-%m-%d')

# Specify desired parameter values for the API query
parameters = {'series_id':'CUSR0000SETG01',
  'observation_date':observation_date,
  'file_type':'json'
 }

# API request
r = fp.fred_api_request(api_key=fp.api_key,path=path,parameters=parameters)

# Return results in JSON format
results = r.json()
#%% Defining common values
inflation_rate = 0.0252         #average inflation rate from 1993 to present
discount_rate = 0.05        #accounting for the time value of money
current_year = datetime.now().year      #default year to use if no input is entered for the year inputs

#%% Defining base functions
def Hist_Airfare():
    """
    Parameters
    ----------
    Menu Option 1: Origin City, Base Year, Comparison Year
    Menu Option 2: Base Year
    Menu Option 3: Base Year
    Menu Option 4: Base Year, Comparison Year, Month of Interest
    Menu Option 5: Base Year
    Menu Option 6: Base Year
    Menu Option 7: No Inputs
    
    Returns
    -------
    Menu Option 1: Inflation-adjusted Real Value Calculator
    Menu Option 2: Historic Best-month-to-travel Search
    Menu Option 3: Historic Monthly Inflation Search
    Menu Option 4: Historic Monthly Inflation Search + Cross-year Comparison
    Menu Option 5: Historic Annual Average Airfare Search
    Menu Option 6: Historic Max/Min Airfare Search
    Menu Option 7: Consumer Price Index (CPI) on Average Airfare
    """
    #Separate Menu function to define menu choices for users
    def menu():
        print('{:s}'.format('-'*100))       #printing separators
        print('MAIN MENU:')
        print('1. Inflation-adjusted Real Value Calculator')
        print('2. Historic Best-month-to-travel Search')
        print('3. Historic Monthly Inflation Search')
        print('4. Historic Monthly Inflation Search + Cross-year Comparison')
        print('5. Historic Annual Average Airfare Search')
        print('6. Historic Max/Min Airfare Search')
        print('7. Consumer Price Index (CPI) on Average Airfare')
        print('8. HELP')
        print('0. QUIT')
        print('{:s}'.format('-'*100))       #printing separators
        choice = input('Enter an integer associated to your feature choice: ')
        print('{:s}'.format('-'*100))       #printing separators
        if choice.isdecimal() and 0 <= int(choice) <= 8:
            return int(choice)
        else:
            print('Invalid choice. Please enter a whole number between 0 and 8.')
    def main():
        while True:
            #Runs menu function for users to input their choice
            choice = menu()
            print('{:s}'.format('-'*100))       #printing separators
            if choice == 0:
                print('Exiting')
                break
            elif choice == 1:
                print('{:s}'.format('-'*100))       #printing separators
                while True:
                    origin_city = input('Enter city:')
                    #Only cities in the airfare_data file can be inputted
                    if origin_city not in (airfare_data['City Name'].values):
                        print('We do not have data for this origin city')
                        continue
                    else:
                        while True: 
                            base_year = input('Enter baseline year:')
                            #If input is None, use current year, else convert input to int
                            if not base_year:
                                base_year = current_year
                                print('Since you have not entered a year, we are using the current year')
                            else:
                                base_year = int(base_year)
        
                            #Restrict user input for years to range program has data for
                            if not 1992 < base_year < current_year:
                                print("Please specify an year between 1993 to {}".format(current_year))
                                continue
                            else:
                                print("You are good")
                                break
                        while True:
                            comp_year = input('Enter comparison year. This is the year you want to compare to the baseline year:')
                            #If input is None, use current year, else convert input to int
                            if not comp_year:
                                comp_year = current_year
                                print('Since you have not entered a year, we are using the current year')
                            else:
                                comp_year = int(comp_year)
        
                            #Restrict user input for years to range program has data for
                            if not 1992 < comp_year < current_year:
                                print("Please specify a date between 1993 to {}".format(current_year))
                                continue
                            else:
                                print("You are good")
                                break
                        #Computing Present Value of Money
                        if base_year - comp_year > 0:
                            present_worth_factor = ((1 + inflation_rate)**(base_year - comp_year))/((1 + discount_rate)**(base_year - comp_year))
                            for_adjusted_value = present_worth_factor * airfare_data[(airfare_data['Year'] == int(base_year)) & (airfare_data['City Name'] == origin_city)]['Average Fare ($)']
                            print('The airfare price', airfare_data[(airfare_data['Year'] == int(base_year)) & (airfare_data['City Name'] == origin_city)]['Average Fare ($)'].iloc[0], 'for', origin_city, 'in', comp_year, 'is', round(for_adjusted_value.iloc[0], 2), 'in', base_year, 'dollars' )
                            break
                        elif base_year - comp_year == 0:
                            print('The years are the same, there is no comparison to be made')
                            break
                        #Computing Future Value of Money 
                        else:
                            future_worth_factor = ((1 + inflation_rate)**(comp_year - base_year))/((1 + discount_rate)**(comp_year - base_year))
                            ba_adjusted_value = airfare_data[(airfare_data['Year'] == int(base_year)) & (airfare_data['City Name'] == origin_city)]['Average Fare ($)']/future_worth_factor
                            print('The airfare price', airfare_data[(airfare_data['Year'] == int(base_year)) & (airfare_data['City Name'] == origin_city)]['Average Fare ($)'].iloc[0], 'for', origin_city, 'in', comp_year, 'is', round(ba_adjusted_value.iloc[0], 2), 'in', base_year, 'dollars' )
                            break
            elif choice == 2:
                print('{:s}'.format('-'*100))       #printing separators
                while True: 
                    base_year = input('Enter baseline year:')
                    #If input is None, use current year, else convert input to int
                    if not base_year:
                        base_year = current_year
                        print('Since you have not entered a year, we are using the current year')
                    else:
                        base_year = int(base_year)

                    #Restrict user input for years to range program has data for
                    if not 1992 < base_year < current_year:
                        print("Please specify a date between 1993 to {}".format(current_year))
                        continue
                    else:
                        print("You are good")
                        break
                #Locating the months with the highest and lowest inflation rates for year inputted
                min_month = airfare_inflation.loc[base_year].idxmin()
                max_month = airfare_inflation.loc[base_year].idxmax()
                print('The best month to travel in', base_year, 'was', min_month)
                print('The worst month to travel in', base_year, 'was', max_month) 
            elif choice == 3:
                print('{:s}'.format('-'*100))       #printing separators
                while True: 
                    base_year = input('Enter baseline year:')
                    #If input is None, use current year, else convert input to int
                    if not base_year:
                        base_year = current_year
                        print('Since you have not entered a year, we are using the current year')
                    else:
                        base_year = int(base_year)
    
                    #Restrict user input for years to range program has data for
                    if not 1992 < base_year < current_year:
                        print("Please specify a date between 1993 to {}".format(current_year))
                        continue
                    else:
                        print("You are good")
                        break
                #Retrieve and plot monthly inflation values for a user-inputted year
                year_inflation = airfare_inflation.loc[base_year, airfare_inflation.columns.drop('Ave')]
                plt.plot(airfare_inflation.columns.difference(['Ave'], sort = False), year_inflation, 'b-', label = 'Monthly Inflation')
                plt.axhline(y = airfare_inflation['Ave'].loc[base_year], color = 'r', label = 'Average Inflation Rate')
                plt.legend()
                plt.xlabel('Month')
                plt.ylabel('Inflation rate(%)')
                plt.show()
            elif choice == 4:
                print('{:s}'.format('-'*100))       #printing separators
                while True: 
                    base_year = input('Enter baseline year:')
                    #If input is None, use current year, else convert input to int
                    if not base_year:
                        base_year = current_year
                        print('Since you have not entered a year, we are using the current year')
                    else:
                        base_year = int(base_year)

                    #Restrict user input for years to range program has data for
                    if not 1992 < base_year < current_year:
                        print("Please specify a date between 1993 to {}".format(current_year))
                        continue
                    else:
                        print("You are good")
                        break
                while True:
                    comp_year = input('Enter comparison year. This is the year you want to compare to the baseline year:')
                    #If input is None, use current year, else convert input to int
                    if not comp_year:
                        comp_year = current_year
                        print('Since you have not entered a year, we are using the current year')
                    else:
                        comp_year = int(comp_year)

                    #Restrict user input for years to range program has data for
                    if not 1992 < comp_year < current_year:
                        print("Please specify a date between 1993 to {}".format(current_year))
                        continue
                    else:
                        print("You are good")
                        break
                while True:
                    month = input('Enter the first three letters of the month you want analyzed:')
                    #If input is None, use current month
                    if not month:
                        month = calendar.month_abbr[datetime.now().month]
                        print('Since you have not entered a month, we are using the current month')
                    #Ensure users only enter abbreviated months
                    months = airfare_inflation.columns.tolist()
                    if month not in months:
                        print('Please specify the month as shown in:', months)
                        continue
                    else:
                        print('You are good')
                        break
                #Compare inflation rates in user inputted date (month, year) to another user inputted date (month, year)
                print('The airfare inflation rate in', month, base_year, 'was', airfare_inflation.loc[base_year, month],
                      'as compared to', airfare_inflation.loc[comp_year, month], 'in', month, comp_year)
            elif choice == 5:
                print('{:s}'.format('-'*100))       #printing separators
                while True: 
                    base_year = input('Enter baseline year:')
                    #If input is None, use current year, else convert input to int
                    if not base_year:
                        base_year = current_year
                        print('Since you have not entered a year, we are using the current year')
                    else:
                        base_year = int(base_year)

                    #Use chained comparison
                    if not 1992 < base_year < current_year:
                        print("Please specify a date between 1993 to {}".format(current_year))
                        continue
                    else:
                        print("You are good")
                        break
                #Determine average fare users are likely to pay in a user inputted year
                airfare_average = airfare_data[(airfare_data['Year'] == int(base_year))]['Average Fare ($)'].mean()
                print('The average annual airfare in ', base_year, 'was', round(airfare_average, 2))
            elif choice == 6:
                print('{:s}'.format('-'*100))       #printing separators
                while True: 
                    base_year = input('Enter baseline year:')
                    #If input is None, use current year, else convert input to int
                    if not base_year:
                        base_year = current_year
                        print('Since you have not entered a year, we are using the current year')
                    else:
                        base_year = int(base_year)

                    #Restrict user input for years to range program has data for
                    if not 1992 < base_year < current_year:
                        print("Please specify a date between 1993 to {}".format(current_year))
                        continue
                    else:
                        print("You are good")
                        break
                #Determine and display max and min airfares in user inputted year for user specified origin cities
                min_airfare = airfare_data[(airfare_data['Year']== int(base_year))]['Average Fare ($)'].min()
                min_city = airfare_data[(airfare_data['Year'] == int(base_year)) & (airfare_data['Average Fare ($)'] == min_airfare)]['City Name']
                max_airfare = airfare_data[(airfare_data['Year']== int(base_year))]['Average Fare ($)'].max()
                max_city = airfare_data[(airfare_data['Year'] == int(base_year)) & (airfare_data['Average Fare ($)'] == max_airfare)]['City Name']
                print('The maximum airfare in', base_year, 'was', max_airfare, 'from', max_city.iloc[0])
                print('The minimum airfare in', base_year, 'was', min_airfare, 'from', min_city.iloc[0])
            elif choice == 7:
                print('{:s}'.format('-'*100))       #printing separators
                # Load data, deal with missing values, format dates in index, and set dtype
                data = pd.DataFrame(results['observations'],columns =['date','value'])
                data = data.replace('.', np.nan)
                data['date'] = pd.to_datetime(data['date'])
                data = data.set_index('date')['value'].astype(float)
                
                print('Plotting CPI Data on average US cities airfares')
                # Plot the unemployment rate
                data.plot()
                plt.title('Consumer Price Index: Average Airline Fares in U.S. Cities')
                plt.grid()
                plt.ylabel('Index, 1982 - 1984 = 100')
                plt.show()
            elif choice == 8:
                print('{:s}'.format('-'*100))       #printing separators
                print('DESCRIPTION:')
                print('1. Compare annual average airfares in real values for two specified years for a specified origin city')
                print('2. Display the least and most expensive months to travel in for a specific year')
                print('3. Plot the monthly inflation rates for a given year')
                print('4. Compare the inflation rates for two specified years within the same months')
                print('5. Compute the annual average fare for a specified year')
                print('6. Display the least and most expensive cities to travel from for a specified year')
                print('7. Plot Consumer Price Index (CPI) data on airfare prices')
    if __name__ == '__main__':
        main()         
Hist_Airfare()              