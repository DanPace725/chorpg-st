import streamlit as st
from db import create_connection, create_tables
from tracker import show_tracker

def main():
    database = "chores.db"
    conn = create_connection(database)
    if conn is not None:
        create_tables(conn)
    else:
        st.error("Error! Cannot create the database connection.")
        return

    show_tracker(conn, 1)

if __name__ == "__main__":
    main()