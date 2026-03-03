import pytz
from datetime import datetime
import streamlit as st

st.title('Time tracker')

time = st.text_area("Copy paste the Today's Attendance logs here", height=200)
ist = pytz.timezone('Asia/Kolkata')
if st.button('Calculate'):
    start = []
    end = []
    for i in time.strip().split('\n'):
        if 'In' in i:
            start.append(i.replace('In','').strip())
        if 'Out' in i:
            end.append(i.replace('Out','').strip())

    now = datetime.now(ist)
    total_sec = 0
    for i,j in zip(start, end):
        t1 = datetime.combine(now.date(),datetime.strptime(i, '%I:%M:%S %p').time())
        t2 = datetime.combine(now.date(),datetime.strptime(j, '%I:%M:%S %p').time())
        total_sec += (t2-t1).total_seconds()
    if len(start) > len(end):
        last_in = datetime.combine(now.date(),datetime.strptime(start[-1], '%I:%M:%S %p').time())
        total_sec += (now - last_in).total_seconds()
    st.success(f"Total working hours: {total_sec // 3600} hours {(total_sec % 3600) // 60} minutes")
    remaining = (((8*3600)+(30*60))-total_sec)
    st.info(f'{remaining//3600} hours left {(remaining%3600)//60} minutes left')

    # st.info(f'{remaining//60} hours left') if remaining > 0 else st.info(f'{remaining} minutes left')
