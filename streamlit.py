from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import streamlit as st

# Indian Standard Time
ist = ZoneInfo("Asia/Kolkata")


def working_hours(input_):

    start = []
    end = []

    # Extract In / Out times
    for i in input_.strip().split('\n'):

        if 'In' in i:
            start.append(i.replace('In', '').strip())

        if 'Out' in i:
            end.append(i.replace('Out', '').strip())

    now = datetime.now(ist)

    total_sec = 0

    # Calculate completed sessions
    for i, j in zip(start, end):

        t1 = datetime.combine(
            now.date(),
            datetime.strptime(i, '%I:%M:%S %p').time(),
            tzinfo=ist
        )

        t2 = datetime.combine(
            now.date(),
            datetime.strptime(j, '%I:%M:%S %p').time(),
            tzinfo=ist
        )

        total_sec += (t2 - t1).total_seconds()

    # If currently logged in
    if len(start) > len(end):

        last_in = datetime.combine(
            now.date(),
            datetime.strptime(start[-1], '%I:%M:%S %p').time(),
            tzinfo=ist
        )

        total_sec += (now - last_in).total_seconds()

    # Working hours
    hours = int(total_sec // 3600)
    minutes = int((total_sec % 3600) // 60)

    st.success(
        f"Total working hours: {hours} hours {minutes} minutes"
    )

    # Remaining time for 8h 30m target
    target_sec = (8 * 3600) + (30 * 60)

    remaining = target_sec - total_sec

    if remaining > 0:

        r_hours = int(remaining // 3600)
        r_minutes = int((remaining % 3600) // 60)

        st.info(
            f"Remaining: {r_hours} hours {r_minutes} minutes left"
        )

        end_time = now + timedelta(seconds=remaining)

        st.info(
            f"Expected logout time: {end_time.strftime('%I:%M:%S %p')}"
        )

    else:
        st.success("Target working hours completed!")


# Streamlit UI
st.title("Time Tracker")

time_logs = st.text_area(
    "Copy paste today's attendance logs here",
    height=250
)

if st.button("Calculate"):

    if time_logs.strip():

        try:
            working_hours(time_logs)

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Please paste attendance logs")
