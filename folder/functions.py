from datetime import datetime

def check_for_zero(x):
    num = []
    x = int(x)
    if x<10:
        for i in str(x):
            number = int(i)
            num.append(number)
        if num[0]!=0:return '0'+ str(x)
        else: return x       
    else: return x

def check_date(datetime_):
    today = datetime.utcnow().date()
    d_ = datetime.strptime(datetime_, "%Y-%m-%d %H:%M:%S")
    date = d_.date()
    check = today > date
    return check
  
def getToday():
    today = datetime.utcnow()
    return today