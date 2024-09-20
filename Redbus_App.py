import streamlit as st
import pymysql
import pandas as pd

# Connect to MySQL database
def get_connection():
    return pymysql.connect(host='127.0.0.1', user='root', passwd='Root', database='red_bus')

# Function to fetch route names starting with a specific letter, arranged alphabetically
def fetch_Route_Name(connection, starting_letter):
    query = f"SELECT DISTINCT Route_Name FROM bus_details WHERE Route_Name LIKE '{starting_letter}%' ORDER BY Route_Name"
    Route_Name = pd.read_sql(query, connection)['Route_Name'].tolist()
    return Route_Name

# Function to fetch data from MySQL based on selected Route_Name and price sort order
def fetch_data(connection, Route_Name, Price_sort_order):
    Price_sort_order_sql = "ASC" if Price_sort_order == "Low to High" else "DESC"
    query = f"SELECT * FROM bus_details WHERE Route_Name = %s ORDER BY Star_Rating DESC, Price {Price_sort_order_sql}"
    df = pd.read_sql(query, connection, params=(Route_Name))
    return df

# Function to filter data based on Star_Rating and Bus_Type
def filter_data(df, star_rating, Bus_type):
    filtered_df = df[df['Star_Rating'].isin(star_rating) & df['Bus_Type'].isin(Bus_type)]
    return filtered_df

# Main Streamlit app
def main():
    st.title("RedBus")
    logo = "D:\RedBus\logo1.png"
    caption_image = "D:\RedBus\Caption Image.png"
    st.header("India's No. 1 Online Bus Ticket Booking Site", divider="gray")
    st.image(caption_image)
    st.sidebar.image(logo, caption='Travel company', use_column_width=True)

    connection = get_connection()

    try:
        # Sidebar - Input for starting letter
        starting_letter = st.sidebar.text_input('Enter starting letter of Route Name', 'A')

        # Fetch route names starting with the specified letter
        if starting_letter:
            Route_name = fetch_Route_Name(connection, starting_letter.upper())

            if Route_name:
                # Sidebar - Selectbox for Route_Name
                selected_route = st.sidebar.radio('Select Route Name', Route_name)

                if selected_route:
                    # Sidebar - Selectbox for sorting preference
                    Price_sort_order = st.sidebar.selectbox('Sort by Price', ['Low to High', 'High to Low'])

                    # Fetch data based on selected Route_Name and price sort order
                    data = fetch_data(connection, selected_route, Price_sort_order)

                    if not data.empty:
                        # Display data table with a subheader
                        st.write(f"### Data for Route: {selected_route}")
                        st.write(data)

                        # Filter by Star_Rating and Bus_Type
                        Star_rating = data['Star_Rating'].unique().tolist()
                        selected_ratings = st.multiselect('Filter by Star Rating', Star_rating)

                        Bus_Type = data['Bus_Type'].unique().tolist()
                        selected_Bus_Type = st.multiselect('Filter by Bus Type', Bus_Type)

                        if selected_ratings and selected_Bus_Type:
                            filtered_data = filter_data(data, selected_ratings, selected_Bus_Type)
                            # Display filtered data table with a subheader
                            st.write(f"### Filtered Data for Star Rating: {selected_ratings} and Bus Type: {selected_Bus_Type}")
                            st.write(filtered_data)
                    else:
                        st.write(f"No data found for Route: {selected_route} with the specified price sort order.")
            else:
                st.write("No routes found starting with the specified letter.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()
