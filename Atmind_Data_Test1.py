import streamlit as st
import pandas as pd
import plotly.express as px

# Load data from GitHub
url = 'https://github.com/oatact/TestJob/raw/main/test_data.csv'
df = pd.read_csv(url, parse_dates=['Order Time', 'Serve Time'], usecols=['Date', 'Order Time', 'Serve Time', 'Menu', 'Price', 'Category', 'Kitchen Staff', 'Drinks Staff', 'Hour', 'Minute', 'Day Of Week'])

# Convert 'Order Time' and 'Serve Time' to datetime format
df['Order Time'] = pd.to_datetime(df['Order Time'], errors='coerce')
df['Serve Time'] = pd.to_datetime(df['Serve Time'], errors='coerce')

# Calculate total sales for each date
total_sales = df.groupby('Date')['Price'].sum().reset_index()

# Calculate the time difference between order and serve times
df['Time Difference'] = (df['Serve Time'] - df['Order Time']).dt.total_seconds() / 60.0  # Convert to minutes

# Count the occurrences of kitchen staff and drink staff
kitchen_performance = df['Kitchen Staff'].value_counts()
drinks_performance = df['Drinks Staff'].value_counts()

# Calculate the total time spent by each staff member
df['Processing Time'] = (df['Serve Time'] - df['Order Time']).dt.total_seconds()
total_time_kitchen = df.groupby('Kitchen Staff')['Processing Time'].sum()
total_time_drinks = df.groupby('Drinks Staff')['Processing Time'].sum()



# Set page title and favicon
st.set_page_config(page_title="Restaurant Analysis Dashboard", page_icon="🍔", layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# Sidebar title and description
st.sidebar.title("Navigation")
st.sidebar.info("Select a page to view")

# Pages in the app
pages = ["All dashboards","Customer Behavior", "Day of the Week Analysis", "Kitchen and Drinks Staff Performance","Menu Composition"]
selected_page = st.sidebar.selectbox("Select a page", pages)

# Main content
st.title("Restaurant Analysis Dashboard")

if selected_page == "All dashboards":

    # Customer Behavior Page

    # Count the occurrences of each food item
    best_sellers = df['Menu'].value_counts()

    # Create a bar chart for best-selling food items using Plotly Express
    fig_Best = px.bar(best_sellers, x=best_sellers.index, y=best_sellers.values, labels={'x': 'Food Item', 'y': 'Quantity'}, title='Best-Selling Items', color_discrete_sequence=['#27AE60'])

    # Customize the layout for the chart
    fig_Best.update_layout(xaxis_title='Food Item', yaxis_title='Quantity')

    # Analyze common preferences during specific hours
    common_preferences_analysis = df.groupby(['Hour', 'Menu']).size().reset_index(name='Frequency')

    # Create a heatmap for common preferences analysis using Plotly Express
    fig_Menu = px.imshow(common_preferences_analysis.pivot_table(index='Menu', columns='Hour', values='Frequency', fill_value=0),
                     labels={'x': 'Hour of the Day', 'y': 'Menu Item', 'color': 'Frequency'},
                     title='Common Preferences Analysis',
                     color_continuous_scale='viridis')

    # Customize the layout for the chart
    fig_Menu.update_layout(xaxis_title='Hour of the Day', yaxis_title='Menu Item')

    col7, col8 = st.columns(2)
    col7.plotly_chart(fig_Best, use_container_width=True)
    col8.plotly_chart(fig_Menu, use_container_width=True)

    visit_frequency = df['Day Of Week'].value_counts()

    # Create a pie chart for visits by day of the week using Plotly Express
    fig2 = px.pie(visit_frequency, names=visit_frequency.index, values=visit_frequency.values, title='Visits by Day of Week')

    # Count the occurrences of orders based on the day of the week
    peak_days_hours_analysis = df.groupby(['Day Of Week', 'Hour']).size().reset_index(name='Number of Orders')

    # Create a bar chart for peak days and hours analysis using Plotly Express
    fig3 = px.bar(peak_days_hours_analysis, x='Hour', y='Number of Orders', color='Day Of Week',
                  labels={'x': 'Hour of the Day', 'y': 'Number of Orders'},
                  title='Peak Days and Hours Analysis', color_discrete_sequence=px.colors.qualitative.Set3)

    # Display the charts side by side using columns
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig2, use_container_width=True)
    col2.plotly_chart(fig3, use_container_width=True)

    #Day of the Week Analysis pages

    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Extract day and week information from the 'Date' column
    df['Day'] = df['Date'].dt.day_name()
    df['Week'] = df['Date'].dt.isocalendar().week

    # Define the order of days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Use Categorical data type with the defined order
    df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)

    # Group by day for the first set of charts
    kitchen_performance = df.groupby(['Day', 'Kitchen Staff']).size().reset_index(name='Number of Orders - Kitchen')
    drinks_performance = df.groupby(['Day', 'Drinks Staff']).size().reset_index(name='Number of Orders - Drinks')

    # Group by week for the second set of charts
    kitchen_performance2 = df.groupby(['Week', 'Kitchen Staff']).size().reset_index(name='Number of Orders - Kitchen')
    drinks_performance2 = df.groupby(['Week', 'Drinks Staff']).size().reset_index(name='Number of Orders - Drinks')

    # Create grouped bar charts
    fig_staff_performance = px.bar(kitchen_performance, x='Day', y='Number of Orders - Kitchen', color='Kitchen Staff',
                                    labels={'x': 'Day', 'y': 'Number of Orders'},
                                    title='Kitchen Staff Performance by Day')

    fig_drinks_performance = px.bar(drinks_performance, x='Day', y='Number of Orders - Drinks', color='Drinks Staff',
                                    labels={'x': 'Day', 'y': 'Number of Orders'},
                                    title='Drink Staff Performance by Day')

    fig_staff_performance2 = px.bar(kitchen_performance2, x='Week', y='Number of Orders - Kitchen', color='Kitchen Staff',
                                    labels={'x': 'Week', 'y': 'Number of Orders'},
                                    title='Kitchen Staff Performance by Week')

    fig_drinks_performance2 = px.bar(drinks_performance2, x='Week', y='Number of Orders - Drinks', color='Drinks Staff',
                                    labels={'x': 'Week', 'y': 'Number of Orders'},
                                    title='Drink Staff Performance by Week')


    # Display the charts using Streamlit
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_staff_performance, use_container_width=True)
    col2.plotly_chart(fig_drinks_performance, use_container_width=True)
    col3, col4 = st.columns(2)
    col3.plotly_chart(fig_staff_performance2, use_container_width=True)
    col4.plotly_chart(fig_drinks_performance2, use_container_width=True)


     #Kitchen and Drinks Staff Performance Page   

    # Count the occurrences of each menu category
    menu_category_counts = df['Category'].value_counts()

    # Create a pie chart for menu composition based on categories
    fig_menu_composition = px.pie(menu_category_counts, names=menu_category_counts.index, values=menu_category_counts.values, title='Menu Composition by Categories', color_discrete_sequence=['#2ca02c', '#d62728'])


    # Count the occurrences of each menu category
    menu_category_counts = df['Category'].value_counts()

# Create a bar chart for the popularity of different menu categories
    fig_category_popularity = px.bar(menu_category_counts, x=menu_category_counts.index, y=menu_category_counts.values, labels={'x': 'Menu Category', 'y': 'Number of Orders'}, title='Popularity of Menu Categories', color_discrete_sequence=['#9467bd'])

# Customize the layout for the chart
    fig_category_popularity.update_layout(xaxis_title='Menu Category', yaxis_title='Number of Orders')

# Display the charts side by side using columns
    col5, col6 = st.columns(2)
    col5.plotly_chart(fig_menu_composition, use_container_width=True)
    col6.plotly_chart(fig_category_popularity, use_container_width=True)



    #Menu competition Page

    # Ensure 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Create a new column for the week number
    df['Week'] = df['Date'].dt.isocalendar().week

    # Count the occurrences of each menu category per week
    weekly_menu_category_counts = df.groupby(['Week', 'Category']).size().reset_index(name='Number of Orders')

    # Create a line chart for the menu composition by categories sold weekly
    fig_weekly_category_sold = px.line(weekly_menu_category_counts, x='Week', y='Number of Orders', color='Category',
                                    labels={'x': 'Week', 'y': 'Number of Orders'},
                                    title='Categories Sold by Week')

    # Customize the layout for the chart
    fig_weekly_category_sold.update_layout(xaxis_title='Week', yaxis_title='Number of Orders')

    # Display the chart
    st.plotly_chart(fig_weekly_category_sold, use_container_width=True)

elif selected_page == "Customer Behavior":
    # Count the occurrences of each food item
    best_sellers = df['Menu'].value_counts()

    # Create a bar chart for best-selling food items using Plotly Express
    fig_Best = px.bar(best_sellers, x=best_sellers.index, y=best_sellers.values, labels={'x': 'Food Item', 'y': 'Quantity'}, title='Best-Selling Items', color_discrete_sequence=['#27AE60'])

    # Customize the layout for the chart
    fig_Best.update_layout(xaxis_title='Food Item', yaxis_title='Quantity')

    # Analyze common preferences during specific hours
    common_preferences_analysis = df.groupby(['Hour', 'Menu']).size().reset_index(name='Frequency')

    # Create a heatmap for common preferences analysis using Plotly Express
    fig_Menu = px.imshow(common_preferences_analysis.pivot_table(index='Menu', columns='Hour', values='Frequency', fill_value=0),
                     labels={'x': 'Hour of the Day', 'y': 'Menu Item', 'color': 'Frequency'},
                     title='Common Preferences Analysis',
                     color_continuous_scale='viridis')

    # Customize the layout for the chart
    fig_Menu.update_layout(xaxis_title='Hour of the Day', yaxis_title='Menu Item')

    col7, col8 = st.columns(2)
    col7.plotly_chart(fig_Best, use_container_width=True)
    col8.plotly_chart(fig_Menu, use_container_width=True)




elif selected_page == "Day of the Week Analysis":
    # Count the occurrences of each day of the week
    visit_frequency = df['Day Of Week'].value_counts()

    # Create a pie chart for visits by day of the week using Plotly Express
    fig2 = px.pie(visit_frequency, names=visit_frequency.index, values=visit_frequency.values, title='Visits by Day of Week')

    # Count the occurrences of orders based on the day of the week
    peak_days_hours_analysis = df.groupby(['Day Of Week', 'Hour']).size().reset_index(name='Number of Orders')

    # Create a bar chart for peak days and hours analysis using Plotly Express
    fig3 = px.bar(peak_days_hours_analysis, x='Hour', y='Number of Orders', color='Day Of Week',
                  labels={'x': 'Hour of the Day', 'y': 'Number of Orders'},
                  title='Peak Days and Hours Analysis', color_discrete_sequence=px.colors.qualitative.Set3)

    # Display the charts side by side using columns
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig2, use_container_width=True)
    col2.plotly_chart(fig3, use_container_width=True)

elif selected_page == "Kitchen and Drinks Staff Performance":
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Extract day and week information from the 'Date' column
    df['Day'] = df['Date'].dt.day_name()
    df['Week'] = df['Date'].dt.isocalendar().week

    # Define the order of days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Use Categorical data type with the defined order
    df['Day'] = pd.Categorical(df['Day'], categories=day_order, ordered=True)

    # Group by day for the first set of charts
    kitchen_performance = df.groupby(['Day', 'Kitchen Staff']).size().reset_index(name='Number of Orders - Kitchen')
    drinks_performance = df.groupby(['Day', 'Drinks Staff']).size().reset_index(name='Number of Orders - Drinks')

    # Group by week for the second set of charts
    kitchen_performance2 = df.groupby(['Week', 'Kitchen Staff']).size().reset_index(name='Number of Orders - Kitchen')
    drinks_performance2 = df.groupby(['Week', 'Drinks Staff']).size().reset_index(name='Number of Orders - Drinks')

    # Create grouped bar charts
    fig_staff_performance = px.bar(kitchen_performance, x='Day', y='Number of Orders - Kitchen', color='Kitchen Staff',
                                    labels={'x': 'Day', 'y': 'Number of Orders'},
                                    title='Kitchen Staff Performance by Day')

    fig_drinks_performance = px.bar(drinks_performance, x='Day', y='Number of Orders - Drinks', color='Drinks Staff',
                                    labels={'x': 'Day', 'y': 'Number of Orders'},
                                    title='Drink Staff Performance by Day')

    fig_staff_performance2 = px.bar(kitchen_performance2, x='Week', y='Number of Orders - Kitchen', color='Kitchen Staff',
                                    labels={'x': 'Week', 'y': 'Number of Orders'},
                                    title='Kitchen Staff Performance by Week')

    fig_drinks_performance2 = px.bar(drinks_performance2, x='Week', y='Number of Orders - Drinks', color='Drinks Staff',
                                    labels={'x': 'Week', 'y': 'Number of Orders'},
                                    title='Drink Staff Performance by Week')

    # Display the charts using Streamlit
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_staff_performance, use_container_width=True)
    col2.plotly_chart(fig_drinks_performance, use_container_width=True)
    col3, col4 = st.columns(2)
    col3.plotly_chart(fig_staff_performance2, use_container_width=True)
    col4.plotly_chart(fig_drinks_performance2, use_container_width=True)
# Add the following code for Menu Composition
elif selected_page == "Menu Composition":
    
  # Count the occurrences of each menu category
    menu_category_counts = df['Category'].value_counts()

    # Create a pie chart for menu composition based on categories
    fig_menu_composition = px.pie(menu_category_counts, names=menu_category_counts.index, values=menu_category_counts.values, title='Menu Composition by Categories', color_discrete_sequence=['#2ca02c', '#d62728'])


    # Count the occurrences of each menu category
    menu_category_counts = df['Category'].value_counts()

# Create a bar chart for the popularity of different menu categories
    fig_category_popularity = px.bar(menu_category_counts, x=menu_category_counts.index, y=menu_category_counts.values, labels={'x': 'Menu Category', 'y': 'Number of Orders'}, title='Popularity of Menu Categories', color_discrete_sequence=['#9467bd'])

# Customize the layout for the chart
    fig_category_popularity.update_layout(xaxis_title='Menu Category', yaxis_title='Number of Orders')

# Display the charts side by side using columns
    col5, col6 = st.columns(2)
    col5.plotly_chart(fig_menu_composition, use_container_width=True)
    col6.plotly_chart(fig_category_popularity, use_container_width=True)

        # Ensure 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Create a new column for the week number
    df['Week'] = df['Date'].dt.isocalendar().week

    # Count the occurrences of each menu category per week
    weekly_menu_category_counts = df.groupby(['Week', 'Category']).size().reset_index(name='Number of Orders')

    # Create a line chart for the menu composition by categories sold weekly
    fig_weekly_category_sold = px.line(weekly_menu_category_counts, x='Week', y='Number of Orders', color='Category',
                                    labels={'x': 'Week', 'y': 'Number of Orders'},
                                    title='Categories Sold by Week')

    # Customize the layout for the chart
    fig_weekly_category_sold.update_layout(xaxis_title='Week', yaxis_title='Number of Orders')

    # Display the chart
    st.plotly_chart(fig_weekly_category_sold, use_container_width=True)


