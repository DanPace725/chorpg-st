import streamlit as st
from db import create_connection, create_tables, get_users, get_tasks, log_activity, get_user_activities, login_admin, get_levels, get_all_user_activities, get_random_small_reward
import pandas as pd
from datetime import datetime
import time


admin_id = 1

def main():
    # Set up the Streamlit page
    st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
    database = "chores.db"
    conn = create_connection(database)
    create_tables(conn)
    
    

def show_tracker(conn, admin_id):
    st.sidebar.title("Chore Tracker")
    
    # Fetching user-specific data
    user_list = get_users(conn, admin_id)
    
    
    user_names = {user[0]: user[1] for user in user_list}
    selected_user_id = st.sidebar.selectbox('Select Child', options=list(user_names.keys()), format_func=lambda x: user_names[x])
    
    current_date = datetime.now().date()
    if selected_user_id:
        display_user_progress(conn, selected_user_id, admin_id, current_date)
        st.sidebar.title("Manage Activities")
        with st.sidebar:
            manage_tasks(conn, selected_user_id, admin_id)
        
    else:
        st.error("Please select a user.")

def display_user_progress(conn, user_id, admin_id, current_date):
    user_details = get_users(conn, admin_id)
    user_details = [user for user in user_details if user[0] == user_id][0]
    user_name, current_level, total_xp = user_details[1], user_details[2], user_details[3]
    
    levels = get_levels(conn, admin_id)
    current_level_info = next((level for level in levels if level[0] == current_level), None)
    next_level_info = next((level for level in levels if level[0] == current_level + 1), None)

    st.title(f"{user_name}'s Chore Progress")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Current Level")
        st.subheader(f"Level {current_level}")

        if current_level_info:
            xp_for_next_level = next_level_info[2]  # Cumulative XP required for next level
        else:
            xp_for_next_level = 100  # Use current level max if there's no next level

        
        # Calculate progress percentage based on total XP against the XP needed for next level
        progress_percent = total_xp / xp_for_next_level if xp_for_next_level else 1
        progress_percent = max(0, min(progress_percent, 1))  # Clamp the value between 0 and 1
        xp_to_next_level = xp_for_next_level - total_xp


        st.progress(progress_percent)
        st.caption(f"{xp_to_next_level} XP to Next Level")

    with col2:
        st.header("Total XP")
        st.subheader(f"{total_xp} XP")


    # Display today's tasks
    today_tasks = get_user_activities(conn, admin_id, user_id, str(current_date))
    if not today_tasks.empty:
        st.header("Today's Tasks")
        st.dataframe(today_tasks)
    else:
        st.write("No tasks for today.")

    # Expander for all tasks
    with st.expander("View All Tasks"):
        all_tasks = get_all_user_activities(conn, admin_id, user_id)
        if not all_tasks.empty:
            st.dataframe(all_tasks)
        else:
            st.write("No tasks found.")
def manage_tasks(conn, user_id, admin_id):
    """Manages tasks and activities for the selected user."""
    task_list = get_tasks(conn, admin_id)
    # Assuming get_tasks returns a list of tuples like [(task_id, task_name), ...]
    task_options = {task[0]: task[1] for task in task_list}  # Create a dictionary to map task IDs to task names
    task_id = st.sidebar.selectbox('Select Task', options=list(task_options.keys()), format_func=lambda x: task_options[x])
    date = st.sidebar.date_input("Date")
    time_spent = st.sidebar.number_input("Time Spent (minutes)", min_value=0, value=0)
    bonus_xp = st.sidebar.number_input("Bonus XP", min_value=0, value=0)
    if st.sidebar.button('Log Task'):
        small_reward = get_random_small_reward(conn)
        log_activity(conn, admin_id, user_id, task_id, str(date), time_spent, bonus_xp, small_reward)
        st.success("Task logged successfully!")
        if small_reward:
            st.toast(f"Congratulations! You earned {small_reward} .")
        
        time.sleep(4)
        st.rerun()

if __name__ == "__main__":
    main()
