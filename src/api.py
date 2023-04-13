from datetime import date
import requests  # needs pip install requests

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
