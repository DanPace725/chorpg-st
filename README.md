# Chore Tracker App

This is a Chore Tracker application built using Streamlit. The app allows parents to track their children's chores, manage tasks, and monitor progress through a gamified system with levels and rewards.

## Features

- **User Management**: Add, update, and delete users (children).
- **Task Management**: Add, update, and delete tasks.
- **Activity Logging**: Log activities for users and track their progress.
- **Progress Dashboard**: Visualize user progress with metrics and charts.
- **Admin Tools**: Manage levels, tasks, and view all data.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/chore-tracker.git
    cd chore-tracker
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run Home.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

## File Structure

- `Home.py`: Main entry point of the application.
- `pages/01_Dashboard.py`: Contains the dashboard page for visualizing user progress.
- `pages/02_Admin.py`: Contains the admin tools for managing users, tasks, and levels.
- `tracker.py`: Contains functions for tracking and displaying user progress.
- `db.py`: Contains database-related functions for managing users, tasks, activities, and levels.

## Dependencies

- `streamlit`
- `plotly`
- `bcrypt`
- `pandas`
- `sqlite3`
