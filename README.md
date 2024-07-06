# Moj Analytics Dashboard

Moj Analytics Dashboard is a comprehensive tool designed to provide insights into user engagement and content trends on the Moj platform. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m flask --app server run
```

## Screenshot
<img width="1434" alt="Screenshot 2024-07-05 at 5 51 15 PM" src="https://github.com/usyntest/moj-analytics-dashboard/assets/68940203/6f5136e3-b264-4061-b2a8-0f059a028b90">

## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Backend**: Python (Flask)
- **Data Source**: Reverse-engineered Moj API for fetching real-time data (due to lack public access).

## Features
- Displays the total number of posts and categorizes content types within a specific query.
- Visualizes the prevalence of languages used in videos.
- Provides real-time snapshots of the most recent posts with metadata.
- Provides insights into the most active accounts based on posts and interactions.
- Summarizes the most popular hashtags by share voice, post count, and interactions.


## NOTE
This project still needs some work like:
- This is very slow due to multiple requests to the API, a friend of mine suggested using multi-threading.
- There can be more work done in reverse engineering Moj's API, with more data it can be improved.
- Using data related to tags can be beneficial in extracting more insights.

Since most of the content on the app is synthesised or taken from another platforms, due to lack of users latest posts are atleast 10-15 days behind 
