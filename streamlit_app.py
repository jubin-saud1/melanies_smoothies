# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col, when_matched
import pandas as pd
# Write directly to the app
st.title(":cup_with_straw: Customise your smoothie! :cup_with_straw:")
st.write(
  """Choose fruits u want in your custom smoothie.
  """
)

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()
#options = st.selectbox('How would you like to be contacted?',
#                       ('Email','Home phone','Mobile phone'))
#st.write('You selected: ' + options)

#fruit = st.selectbox('Whai is your favorite fruit?',
#                       ('Banana','Strawberries','Peaches'))
#st.write('You selected: ' + fruit)
name_on_order = st.text_input('Name on Smoothie ?')
st.write('The name on smoothie will be - ',name_on_order)




my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop

#convert snowflake df into pandas df
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list =  st.multiselect(
    'Select upto 5 ingridients', 
    my_dataframe,
    max_selections=5)

if ingredients_list:
    #st.write(my_ingredients)
    #st.text(my_ingredients)

    ingredients_string = ''
    for fruits in ingredients_list:
        ingredients_string += fruits + ' '
      
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits,' is ', search_on, '.')

      
        st.subheader(fruits + ' nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        #st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")




