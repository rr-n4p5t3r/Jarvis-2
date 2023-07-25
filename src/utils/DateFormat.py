import datetime

class DateFormat():

    @classmethod
    def convert_date(self, date):
        return datetime.datetime.strftime(date, '%d-%m-%Y %H:%M:%S%z')