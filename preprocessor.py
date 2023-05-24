import re
import pandas as pd
def preprocess(data):
    pattern = '(\d{2}\/\d{2}\/\d{4}, \d*:\d{2}).[AaPp][Mm]\s-\s'
    pattern2 = '\d{2}\/\d{2}\/\d{4}, \d*:\d{2}.[AaPp][Mm]\s-\s'
    messages = re.split(pattern2,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({"User_message":messages,"message_date":dates})
    # Convert df date column type
    df['message_date'] = pd.to_datetime(df['message_date'],format='%d/%m/%Y, %H:%M')
    df.rename(columns={'message_date':'date'},inplace=True)

    # Separate user and messages
    users = []
    messages = []
    for message in df['User_message']:
        entry = re.split('([\w\W]*?):\s',message)
        if entry[1:]:  #user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['User_message'],inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df["date"].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df["date"].dt.month_name()
    df['day'] = df["date"].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df["date"].dt.hour
    df['minute'] = df["date"].dt.minute

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if 'hour' == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str(hour) + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period'] = period

    return df