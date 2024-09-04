import datetime
import calendar
import zoneinfo
import ics
import yaml
tz = zoneinfo.ZoneInfo('Europe/Paris')
def read_file(path):
    return yaml.dump_all()

def read(file):
    data={}
    with open(file, 'r') as file:
        data = yaml.safe_load(file)
    return data

def daterange_not_weekend(start_date: datetime.date, days):
    for n in range(days):
        date=start_date + datetime.timedelta(n)
        day_in_week=calendar.weekday(date.year,date.month,date.day)
        if day_in_week not in (calendar.SATURDAY,calendar.SUNDAY):
            yield date

def add_event(calendar,name,begin,end):
    e = ics.Event(name,begin,end)
    calendar.events.add(e)
def save(file,cal):
    with open(file, "w") as f:
        f.write(cal.serialize())
def compute_timerange(timerangelist,day):
    timerange=[0,0]
    for i,timerangestr in enumerate(timerangelist):
        hours_str,minutes_str=timerangestr.split('h')
        hour=int(hours_str)
        if minutes_str=="":
            minutes_str='0'
        minute=int(minutes_str)
        time=datetime.time(hour,minute,tzinfo=tz)
        timerange[i]=datetime.datetime.combine(day,time)
    return timerange

def compute_event(cal,data_event,day):
    begin,end=compute_timerange(data_event["heure"],day)
    salle=data_event["salle"]
    name=data_event["name"]
    title=f'{name} : {salle}'
    add_event(cal,title,begin,end)

def compute_data(data):
    cal=ics.Calendar()
    first_day=datetime.date(2024,9,5) #jour de depart
    n_days=len(data)
    print(n_days)
    for day,data_day in zip(daterange_not_weekend(first_day,n_days),data):
        for data_event in data_day:
            compute_event(cal,data_event,day)
    save("out.ics",cal)
def main():
    file='edt.yaml'
    data:list=read(file)
    compute_data(data)

if __name__=="__main__":
    main()
