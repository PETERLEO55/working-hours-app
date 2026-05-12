import pytz
from datetime import datetime, timedelta
import streamlit as st

ist = pytz.timezone('Asia/Kolkata')

def working_hours(input_):
    start = []
    end = []
    for i in input_.strip().split('\n'):
        if 'In' in i:
            start.append(i.replace('In','').strip())
        if 'Out' in i:
            end.append(i.replace('Out','').strip())

    time_now = datetime.now(ist)
    total_sec = 0
    for i,j in zip(start, end):
        t1 = datetime.combine(time_now.date(),datetime.strptime(i, '%I:%M:%S %p').time())
        t2 = datetime.combine(time_now.date(),datetime.strptime(j, '%I:%M:%S %p').time())
        total_sec += (t2-t1).total_seconds()
    if len(start) > len(end):
        last_in = datetime.combine(time_now.date(),datetime.strptime(start[-1], '%I:%M:%S %p').time())
        total_sec += (time_now - last_in).total_seconds()
    st.info(f"Total working hours: {total_sec // 3600} hours {(total_sec % 3600) // 60} minutes")
    remaining = (((8*3600)+(30*60))-total_sec)
    st.info(f'Remaining: {remaining//3600} hours left {(remaining%3600)//60} minutes left')
    r_hours,r_minutes = remaining // 3600,(remaining % 3600) // 60
    remaining = timedelta(hours=r_hours, minutes=r_minutes)
    now = datetime.now()
    end_time = now + remaining
    st.info("End time:", end_time.strftime('%I:%M:%S %p'))


st.title('Time tracker')

time = st.text_area("Copy paste the Today's Attendance logs here", height=200)

if st.button('Calculate'):
    working_hours(time)
