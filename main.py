import requests  # needs pip install requests
from tabulate import tabulate   # needs pip install tablulate
from datetime import date
import os  # import operating system routines


''' RequestParmaters - An instance of this class is used for passing
    parameters to RequestInfo constructor
'''


class RequestParameters:
    def __init__(self, number_of_days, city) -> None:
        self.number_of_days = number_of_days
        self.city = city


"""
    RequestInfo
    DESCRIPTIOIN: Helps creating and sending HTTP-Requests to the API 
"""


class RequestInfo:
    def __init__(self, parameters) -> None:

        if not isinstance(parameters, RequestParameters):
            return None
        self.API_KEY = "?key=288ee8558204498d9cf04212230604"
        self.QUERY = "&q=" + parameters.city
        self.FORECAST_SPAN = "&days=" + str(parameters.number_of_days)
        self.BASE_URL = "http://api.weatherapi.com/v1/forecast.json"
        self.CURL = self.BASE_URL + self.API_KEY + self.QUERY \
            + self.FORECAST_SPAN
        # x = requests.get('https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m')

    ''' Get Response from API and assemble a ResponseInfo object and return it
    PARAMETER: temperature_unit
    VALUES : 'f' for Fahrehneit or 'c' for Celcius
    Deliver Fahrenheit or Celcius Readings
    RETURN: Object of type ResponseInfo, which contains a map, that is retrieved from
    a JSON-file. The map contains all the weather-data received from the API
    '''

    def getRespoonse(self, temperature_unit):
        day = 0
        response = ResponseInfo()
        x = requests.get(self.CURL)
        json_obj = x.json()
        if temperature_unit == 'f':
            current_temperature = json_obj['current']['temp_f']
        else:
            current_temperature = json_obj['current']['temp_c']
        response.response_table[day]['current_temperature'] = current_temperature
        response.response_table[day]['date']\
            = self.extract_date(json_obj['location']['localtime']
                                )
        for first_layer in json_obj:
            for second_layer in json_obj[first_layer]:
                if second_layer == 'forecastday':
                    for day_info in json_obj[first_layer][second_layer]:
                        # Avarage temperature for each day
                        # avg_tmp = str(day_info['day']['avgtemp_f'])
                        # The date has already been added to the first element
                        # before the loop, so skip the first entry
                        if day > 0:
                            date = self.extract_date(day_info['date'])
                            # add date of the current element to response
                            response.response_table[day]['date'] = date
                        # print("DATE: " + date)
                        # print("AVARAGE TEMPERATURE: " + avg_tmp)
                        # add hourly report for the current element to respoonse
                        for hourly in day_info['hour']:
                            # plain_time = self.extract_time(str(hourly['time']))
                            # print("time: " + plain_time + "   " +
                            #       "temperature: " + str(hourly['temp_f']))
                            if temperature_unit == 'f':
                                response.response_table[
                                    day]['hourly'].append(
                                    str(hourly['temp_f']) + " "
                                    + temperature_unit.upper() + " "
                                    + hourly['condition']['text'])
                            else:
                                response.response_table[
                                    day]['hourly'].append(
                                    str(hourly['temp_c']) + " "
                                    + temperature_unit.upper() + " "
                                    + hourly['condition']['text'])
                        # Increment the current element index
                        day += 1
                        # Add another dictionary to the list in the response
                        response.nextDay()
        return response

    def extract_date(self, timestamp):
        """Extracts the date from a timestamp


        Args:
            timestamp (string):The string is formatted like so: "2024/04/01 14:00:00:00"

        Returns:
            string: The date extracted from the timestamp, which will look like this: "Mon.1.Apr"
        """
        data = timestamp.split(" ")
        data_split = data[0].split("-")
        data_year = int(data_split[0])
        data_month = int(data_split[1])
        data_day = int(data_split[2])
        date_obj = date(data_year, data_month, data_day)
        date_as_str = ""
        data_weekday = self.getWeekdayName(date_obj)
        date_as_str = data_weekday + " " + str(data_day) + "."\
            + self.getMonthName(data_month)

        return date_as_str

    def getWeekdayName(self, date):
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        return weekdays[date.weekday()]

    def getMonthName(self, month_as_int):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return months[month_as_int]


class ResponseInfo:
    def __init__(self) -> None:
        current_day = {'current_temperature': '', 'date': '', 'hourly': []}
        self.response_table = []
        self.response_table.append(current_day)

    def nextDay(self):
        next_row = {'date': '', 'hourly': []}
        self.response_table.append(next_row)


class TextTable:
    def __init__(self, columns) -> None:
        self.cols = columns
        self.table = []
        for i in range(25):
            self.table.append([])

    def addHeader(self, column_index,  text):
        pass

    def addCellToColumn(self, column_index, text):
        pass

    def addCellToRow(self, text):
        pass

    def printTable(self):
        # Headings
        print(chr(0x2554) + chr(0x2550) * 20 +
              chr(0x2566) + chr(0x2550) * 20 + chr(0x2557))
        print(chr(0x2551) + " " * 20 + chr(0x2551) + " " * 20 + chr(0x2551))
        print(chr(0x255a) + chr(0x2550) * 20 +
              chr(0x2569) + chr(0x2550) * 20 + chr(0x255d))
        # Cells
        print(chr(0x250c) + chr(0x2500) * 20 +
              chr(0x252c) + chr(0x2500) * 20 + chr(0x2510))
        print(chr(0x2502) + " " * 20 + chr(0x2502) + " " * 20 + chr(0x2502))
        print(chr(0x2514) + chr(0x2500) * 20
              + chr(0x2534) + chr(0x2500) * 20 + chr(0x2518))

        table = [['col1', 'col2'], [1, 2], [3, 4]]
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    def printForcast(self, response_info):
        self.addHoursColumn()
        self.addForecastColumns(response_info=response_info)
        print(tabulate(self.table, headers='firstrow', tablefmt='fancy_grid'))

    def printTodaysForecast(self, response_info):
        pass

    def addHoursColumn(self):
        for i in range(25):
            if i == 0:
                self.table[i].append("TIME")
            elif i <= 9 and i > 0:
                self.table[i].append("0" + str(i) + ":00")
            else:
                self.table[i].append(str(i) + ":00")

    def addForecastColumns(self, response_info):
        for response_table_index in range(len(response_info.response_table)):
            entry_index = 1
            self.table[0].append(
                "DATE: " + str(response_info.response_table[response_table_index]['date']))
            for hourly in response_info.response_table[response_table_index]['hourly']:
                self.table[entry_index].append(hourly)
                # Go to the next entry
                entry_index += 1


class UserInterface:
    def __init__(self) -> None:
        self.EXIT = False
        # Number of days to be convered in the forecast
        self.FORECAST_SPAN = 7
        # Which temperature unit should be displayed
        self.TEMPERATURE_UNIT = 'f'
        self.NAME_OF_CITY = "Berlin"
    # Show the current temperature

    def showCurrentTemperature(self):
        # Table that holds the data to be printed
        table = []
        # Parameters for the RequestInfo constructor
        parameters = RequestParameters(number_of_days=1, city="Berlin")
        # Create an instance of RequestInfo, which will in turn
        # send a request to the online API
        info = RequestInfo(parameters=parameters)
        # Extract the response, received from the API
        res = info.getRespoonse(self.TEMPERATURE_UNIT)
        curr_temp = str(res.response_table[0]['current_temperature'])
        if self.TEMPERATURE_UNIT == 'f':
            curr_temp = str(curr_temp) + " F"
        else:
            curr_temp = str(curr_temp) + " C"
        curr_date = str(res.response_table[0]['date'])
        table.append([])
        table[0] = ["CURRENT DATE: ", "CURRENT TEMPERATURE: "]
        table.append([])
        table[1] = [curr_date, curr_temp]
        # clear the screen before showing the data
        self.clearScreen()
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    """Print the forecast for the current day """

    def printTodaysForecast(self):
        parameters = RequestParameters(
            number_of_days=1, city=self.NAME_OF_CITY)
        info = RequestInfo(parameters=parameters)
        res = info.getRespoonse(self.TEMPERATURE_UNIT)
        # clear the screen beofore printing the forecast
        self.clearScreen()
        t = TextTable(1)
        t.printForcast(response_info=res)

    def printForecast(self, number_of_days):
        tables = []
        table_index = 0
        parameters = RequestParameters(number_of_days=self.FORECAST_SPAN,
                                       city=self.NAME_OF_CITY)
        info = RequestInfo(parameters=parameters)
        res = info.getRespoonse(self.TEMPERATURE_UNIT)
        for index in range(len(res.response_table)):
            # assemple the headers of the table
            tables.append([])
            tables[table_index].append(
                ['DATE',
                 res.response_table[index]['date']])
            hour = 0
            for time in res.response_table[index]['hourly']:
                str_temp = str(time)
                str_time = str(hour) + ":00 "
                # assemple next row of the table
                tables[table_index].append([str_time, str_temp])
                # next hour
                hour += 1
            # next teble
            table_index += 1

        # clear the screen beofore printing the forecast
        self.clearScreen()
        # test the table class
        t = TextTable(7)
        t.printForcast(response_info=res)

    def printTable(self):
        table = TextTable(2)
        table.printTable()

    # Starting point
    def main(self):
        self.getSettings()
        # Clear the screen when starting up
        self.clearScreen()
        while self.EXIT is False:
            self.getUserInput()

    # Process user's input

    def getUserInput(self):
        self.printSwitchBoard()
        _input = input("Enter command: ")
        if _input.lower() == "exit":
            self.EXIT = True
        elif _input.lower() == "today":
            self.printTodaysForecast()
        elif _input.lower() == "forecast":
            self.printForecast(self.FORECAST_SPAN)
        elif _input.lower() == "current":
            self.showCurrentTemperature()
        elif _input.lower() == "get settings":
            self.getSettings()
        elif _input.lower() == "set tu":
            self.setTemperatureUnit()
        elif _input.lower() == "set fs":
            self.setForecastSpan()
        elif _input.lower() == "update":
            self.updateSettings()
        elif _input.lower() == "table":
            self.printTable()

    # Set the preferred temperature unit
    # User can choose between Fahrenheit and Celcius

    def setTemperatureUnit(self):
        unit = input("Enter temperature unit [ F / C ] :")
        if unit.lower() == 'f' or unit.lower() == 'c':
            self.TEMPERATURE_UNIT = unit
            if unit.lower() == 'c':
                print("Temperature Unit set to Celcius!")
            else:
                print("Temperature Unit set to Fahrenheit!")
        else:
            print("You can only put F for Fahrenheit or C for Celicius!")

    def setForecastSpan(self):
        days = input("Enter number of days: ")
        setting = 0
        if days.isnumeric():
            if int(days) > 7:
                setting = 7
                print("Maximum span is 7 days, current setting is now 7 days!")
            else:
                setting = int(days)
            self.FORECAST_SPAN = setting
            self.updateSettings()
            print(f'Forecast span set to {days} days!')
        else:
            print("Number of days must be a number!")

    def updateSettings(self):
        file_content = "tu=" + self.TEMPERATURE_UNIT + \
            " " + "days=" + str(self.FORECAST_SPAN)
        path = os.path.normcase("./conf/settings.sf")
        f = open(path, "w")
        f.write(file_content)
        f.close()
        print("Settings have been updated!")

    # Read settings from the file
    def getSettings(self):
        try:
            path = os.path.normcase("./conf/settings.sf")
            f = open(path, "r")
            file_content = f.read()
            split_content = file_content.split(" ")
            tu = split_content[0].split("=")
            days = split_content[1].split("=")
            self.TEMPERATURE_UNIT = tu[1]
            self.FORECAST_SPAN = int(days[1])
        except FileNotFoundError:
            # Create settings-file using default values
            self.updateSettings()

    def printSwitchBoard(self):
        swtich_board = []
        swtich_board.append([])
        swtich_board[0] = ['DESCRIPTION', 'COMMAND']
        swtich_board.append([])
        swtich_board[1] = ['Show the forcast for the number of days, defined in the settings. \nDefault is 7 days, and temperature unit defaults to Fahreinheit!',
                           'forecast']
        swtich_board.append([])
        swtich_board[2] = ['Show the forcast for today', 'today']
        swtich_board.append([])
        swtich_board[3] = ['Current temperature', 'current']
        swtich_board.append([])
        swtich_board[4] = [
            'Set the temperature unit[Celcius/Fahrenheit]', 'set tu']
        swtich_board.append([])
        swtich_board[5] = [
            'Set the span of a forecast. How many days to cover? Maximum is 7!', 'set fs']

        print(tabulate(swtich_board, headers='firstrow', tablefmt='fancy_grid'))

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')


user = UserInterface()
user.main()
