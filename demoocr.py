import easyocr as ocr    
import streamlit as st   
from PIL import Image   
import numpy as np       
import pandas as pd
import regex as re
import mysql.connector
from mysql.connector import Error

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bizcard")
mycursor = mydb.cursor(buffered=True)
mycursor.execute("CREATE TABLE IF NOT EXISTS businessdata (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), job_title VARCHAR(255), address VARCHAR(255), postcode VARCHAR(255), phone VARCHAR(255), email VARCHAR(255), website VARCHAR(255), company_name VARCHAR(225))")

st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://yt3.ggpht.com/a/AATXAJyg0HC-wti-ZbydRiNojQ3WzbxM8N_FcOtJtdfwAg=s900-c-k-c0xffffffff-no-rj-mo");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
         
        )

st.title("**:blue[BizCardX: Extracting Business Card Data with OCR]**")
st.markdown("#### :violet[Optical Character Recognition - Using OCR,Streamlit GUI & SQL]")


menu = ['','Upload','View','Update','Delete']
choice = st.sidebar.selectbox("Choose an option",menu)



if choice == "Upload":
    image = st.file_uploader(label = ":violet[Upload your business card here]",type=['png','jpg','jpeg'])
    @st.cache_data
    def load_model(): 
        reader = ocr.Reader(['en'],model_storage_directory='.')
        return reader
    reader = load_model() 
    if image is not None:
        input_image = Image.open(image) 
        st.image(input_image) 
        with st.spinner("🤖 The image has been processing! "):
            result = reader.readtext(np.array(input_image))
            result_text = [] 
            for text in result:
                result_text.append(text[1])
            st.write(result_text)
            st.write("**:violet[EXTRACTED INFORMATION FROM BUSINESS CARD]**")
            st.write("Name:", result_text[0])
            st.write("Job Title:", result_text[1])
            st.write("Address:", result_text[2])
            st.write("Postcode:", result_text[3])
            st.write("Phone:", result_text[4])
            st.write("Email:", result_text[5])
            st.write("Website:", result_text[6])
            st.write("company_name:", result_text[7])
            st.success("Business Card Details extracted successfully !!")
            st.balloons()
            if st.button("Insert into SQL Database"):
                sql = "INSERT INTO businessdata(name, job_title, address, postcode, phone, email, website, company_name) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (result_text[0], result_text[1], result_text[2], result_text[3], result_text[4], result_text[5], result_text[6], result_text[7])
                mycursor.execute(sql, val)
                mydb.commit()
                st.success("Business card information uploaded to database.")
    else:
        st.write("Upload an Image")


elif choice == "View":
    st.write(":violet[Data retrived from Database]")
    mycursor.execute("SELECT * FROM businessdata")
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=['id','name', 'job_title', 'address', 'postcode', 'phone', 'email', 'website', 'company_name'])
    st.write(df)

elif choice == "Update":
    mycursor.execute("SELECT * from businessdata")
    result = mycursor.fetchall()
    business_data = {}
    for i in result:
        business_data[i[1]] = i[0]
    selected_card_name = st.selectbox("Choose the card to be updated",list(business_data.keys()))
    mycursor.execute("SELECT * from businessdata WHERE name=%s",(selected_card_name,))
    result = mycursor.fetchone()

    st.write(":violet[Update the selected card details]")
    name = st.text_input("Name", result[1])
    job_title = st.text_input("Job Title", result[2])
    address = st.text_input("Address", result[3])
    postcode = st.text_input("Postcode", result[4])
    phone = st.text_input("Phone", result[5])
    email = st.text_input("Email", result[6])
    website = st.text_input("Website", result[7])
    company_name = st.text_input("Company Name", result[8])
    if st.button("Update business card details in database"):
        mycursor.execute("UPDATE businessdata SET name=%s,job_title=%s,address=%s,postcode=%s,phone=%s,email=%s,website=%s,company_name=%s WHERE name=%s",
                         (name,job_title,address,postcode,phone,email,website,company_name,selected_card_name))
        mydb.commit()
        st.success("Business card details updated in the database")


elif choice == 'Delete':
    mycursor.execute("SELECT id, name FROM businessdata")
    result = mycursor.fetchall()
    business_data = {}
    for j in result:
        business_data[j[0]] = j[1]
    selected_card_id = st.selectbox("Choose the business card to delete", list(business_data.keys()), format_func=lambda x: business_data[x])
    mycursor.execute("SELECT name FROM businessdata WHERE id=%s", (selected_card_id,))
    result = mycursor.fetchone()
    selected_card_name = result[0]
    

    # Display the current information for the selected business card
    st.write(":violet[Delete the selected business card] ", selected_card_name)
    if st.button("Delete Business Card"):
        mycursor.execute("DELETE FROM businessdata WHERE name=%s", (selected_card_name,))
        mydb.commit()
        st.success("Business card details deleted from database.")


st.caption("Made with ❤️ by aspiring Data Analyst Yamuna G ")


