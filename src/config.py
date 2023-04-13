import os  # import operating system routines


class Configuration:
    def updateSettings(self, temp_unit, forecast_span):
        file_content = "tu=" + temp_unit + \
            " " + "days=" + str(forecast_span)
        path = os.path.normcase("./conf/settings.sf")
        f = open(path, "w")
        f.write(file_content)
        f.close()
        data = {'temperature_unit': temp_unit, 'forecast_span': forecast_span}
        return data

    # Read settings from the file
    def getSettings(self):
        data = {'temperature_unit': '', 'forecast_span': 0}
        try:
            path = os.path.normcase("./conf/settings.sf")
            f = open(path, "r")
            file_content = f.read()
            split_content = file_content.split(" ")
            tu = split_content[0].split("=")
            days = split_content[1].split("=")
            data["temperature_unit"] = tu[1]
            data["forecast_span"] = int(days[1])
            return data
        except FileNotFoundError:
            # Create settings-file using default values
            return self.updateSettings(temp_unit='f', forecast_span=7)
