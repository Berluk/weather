from datetime import datetime
import calendar


class GetDay:

    @classmethod
    def convert_utc_time(cls, unix_time):
        time = int(unix_time)
        date = datetime.utcfromtimestamp(time).strftime('%d %m %Y')
        month_name = calendar.month_name[datetime.utcfromtimestamp(time).date().month]
        days = datetime.strptime(date, '%d %m %Y').weekday()
        day_name = calendar.day_name[days]
        return day_name, month_name
