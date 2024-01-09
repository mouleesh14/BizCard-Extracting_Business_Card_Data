import streamlit as st  # This package is used to built the streamlit application
import cv2  # Used to read the image 
from PIL import Image
import easyocr  # Used to extract the text from the image
import numpy as np  # To perform mathametical operation
import os  # Used to file from the local systems
import re  # To macth the string to the given pattern
import mysql.connector  # To connect the mysql database
import pandas as pd

st.set_page_config(layout='wide',page_title="Bizcard")
reader = easyocr.Reader(['en'])
final=[]

#It displays the table form the MYSQL database
def display():
    connect= mysql.connector.connect(host="localhost",user="root",password="Moulee009",autocommit=True)
    mycursor=connect.cursor()
    mycursor.execute("use bizcard")
    query="""select * from bizcard_datas"""
    mycursor.execute(query)
    details=mycursor.fetchall()
    df=pd.DataFrame(details,columns=["Name","Desgination","Phone_no","Email","Website","Street","City","State","Pincode","Company"])
    return df

#Cleaning the text from the image and inserting the values in MYSQL database 
def filter_value(result1):
    try:
        for h in result1:
            datas={"Name":[],"Desgination":[],"Phone_no":[],"Email":[],"Website":[],"Street":[],"City":[],"State":[],"Pincode":[],"Company":[]}
            ad=h.copy()
            for i in h:
                if i in h[0]:
                    ad.pop(ad.index(i))
                    datas["Name"].append(i)
                if i in h[1]:
                    ad.pop(ad.index(i))
                    datas["Desgination"].append(i)
                if (len(re.findall('\d',i))==10):
                    ad.pop(ad.index(i))
                    datas["Phone_no"].append(i)
                if re.findall("^\w+\@.*\.\w+$",i):
                    ad.pop(ad.index(i))
                    datas["Email"].append(i)
                if re.findall("\w+\.\w+",i) and "@" not in i:
                    ad.pop(ad.index(i))
                    datas["Website"].append(i)
                if re.findall("^[\d+\/\d+\,-]+\s[\w+\,-]+",i):
                    add=i.split(',')
                    for k in add:
                        if k.isspace() or len(k)<1:
                            add.remove(k)
                    if len(add)==1:
                        datas["Street"].append(add[0])
                    elif len(add)==2:
                        datas["Street"].append(add[0])
                        datas["City"].append(add[1])
                    elif len(add)==3:
                        datas["Street"].append(add[0])
                        datas["City"].append(add[1])
                        datas["State"].append(add[2])
                    ad.pop(ad.index(i))
                if re.findall("^\w+\s\d{6}",i):
                    aw=i.split()
                    if len(aw)==1:
                        datas["State"].append(aw[0])
                    elif len(aw)==2:
                        datas["State"].append(aw[0])
                        datas["Pincode"].append(aw[1])
                    ad.pop(ad.index(i))
                if re.findall(r'^\d{6}', i):
                    ad.pop(ad.index(i))
                    datas["Pincode"].append(i)
                if i in h[-1]:
                    if len(i)>4:
                        ad.pop(ad.index(i))
                        datas["Company"].append(i)
                    else:
                        g=h[-2]
                        ad.pop(ad.index(g))
                        datas["Company"].append(h[-2])
            for o in datas:
                if len(datas[o])==0:
                    for s in ad:
                        if len(s)>4 or "," in s:
                            datas[o].append(s)
                    continue
            val=[]
            for l in datas:
                if len(datas[l])>1:
                    val1=' '.join(datas[l])
                    print(val1)
                    val.append(val1)
                else:
                    val.append(datas[l][0])
            val=[val]
            connect= mysql.connector.connect(host="localhost",user="root",password="Moulee009",autocommit=True)
            mycursor=connect.cursor()
            mycursor.execute("use bizcard")
            try:
                mycursor.execute("create table bizcard_datas (Name varchar(20),Desgination varchar(20), Phone_no varchar(50),Email varchar(20),Website varchar(20),Street varchar(20),City varchar(20),State varchar(20),Pincode varchar(20),Company varchar(20),UNIQUE (Email))")
            except:
                pass
            query="""insert into bizcard_datas values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            mycursor.executemany(query,val)
        return True
    except Exception as e:
        st.exception(e)
    

st.markdown("<h1><FONT COLOR='#035096'>Bizcard</h2>",unsafe_allow_html=True)
with st.expander("About"):
    st.markdown("<h3><FONT COLOR='#32527b'>Bussiness Card</h3>",unsafe_allow_html=True)
    st.write("A business card is a compact, printed representation of essential contact information and professional identity. Typically measuring around 3.5 inches by 2 inches, this small but powerful tool serves as a tangible introduction and connection between individuals in the business world. Business cards are exchanged during formal introductions, networking events, and business meetings ")
    st.write("""<b>Contact Information:</b> Includes the individual's name, job title, company name, phone number, email address, and physical address.
    
<b>Logo and Branding:</b> Often displays the company logo and branding elements to reinforce brand identity.
    
<b>Design and Aesthetics:</b> Business cards come in various designs, colors, and finishes to make a memorable visual impact. A well-designed card reflects professionalism and attention to detail.
    
<b>Purposeful Details:</b> May include additional details such as a tagline, social media handles, or a QR code linking to a website or online portfolio.""",unsafe_allow_html=True)
    image_card=Image.open("D:/Python/image/1.png")
    st.image(image_card, caption='This is an sample Business card image',width=800,)
    st.markdown("<h3><FONT COLOR='#32527b'>About Project</h3>",unsafe_allow_html=True)
    st.write("""<b>Time Efficiency:</b>
    BizCardX drastically reduces the time spent manually inputting business card data, allowing users to focus on building connections and growing their network.
    
<b>Accuracy and Reliability:</b>
    With its advanced OCR technology, BizCardX ensures a high level of accuracy in extracting and organizing business card information.
    
<b>Accessibility:</b>
    Access your digitized contacts anytime, anywhere, fostering increased flexibility and convenience for professionals on the go.
    
<b>Seamless Integration:</b>
    Integrate BizCardX effortlessly into your existing workflow, connecting it with your preferred productivity tools for a unified experience.
    
<b>Professional Image:</b>
    Present a modern and tech-savvy image by adopting BizCardX for efficient business card management, showcasing your commitment to innovation in networking.""",unsafe_allow_html=True)

st.write("""<h4><FONT COLOR='#32527b'>You can select one option to preform the task</h5>""",unsafe_allow_html=True)
radio=st.radio("Choose one option: ",options=["Browse image","Choose path"])
if radio=="Browse image":
    st.markdown("<h3><FONT COLOR='#32527b'>Browse Image</h3>",unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Insert", "Modify", "Delete"])
    with tab1:
        st.write("1. You can browse your images from your local files system and you can able to select the image one by one")
        st.write("2. After selecting the image, Click the Submit button to perform the task")
        st.write("3. It will Extract the text from the selected image and it will clean the text from the image ")
        st.write("4. After the cleaning process it will insert the extracted text to MYSQL database ")
        on = st.toggle('View Data',key="tog1")
        if on:
            data_frame=display()
            st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
            st.dataframe(data_frame,hide_index=True)
        input_file=st.file_uploader("Select an image: ", type=["jpg", "jpeg", "png"])
        if st.button("Submit",key="btn1"):
            image = Image.open(input_file)
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            result = reader.readtext(opencv_image,detail=0)
            result=[result]
            yes=filter_value(result)
            if yes:
                st.write("""<h3><FONT COLOR='#32CD32>Inserted successfully..</h3>""",unsafe_allow_html=True)
                data_frame=display()
                st.write("<h4>Successfully inserted...</h4>",unsafe_allow_html=True)
                st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                st.dataframe(data_frame,hide_index=True)
        
    with tab2:
        st.markdown("<h3><FONT COLOR='#32527b'>Update Datas</h3>",unsafe_allow_html=True)
        st.write("1. You can able to change the values in the database")
        st.write("2. Enter the Email Id to modify the values")
        st.write("3. After given the email you have to specify the column name to modify")
        st.write("4. After specifying the column name enter the original data to change")
        on = st.toggle('View Data',key="tog2")
        if on:
            data_frame=display()
            st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
            st.dataframe(data_frame,hide_index=True)
        c1,c2,c3=st.columns(3)
        with c1:
            email=st.text_input("Enter the Email id: ")
        with c2:
            column=st.text_input("Enter the column name that you want to edit: ")
        with c3:
            value=st.text_input("Enter the data: ")
        if st.button("Modify"):
            query=f"""update bizcard_datas SET {column} = '{value}' WHERE Email = '{email}'"""
            connect= mysql.connector.connect(host="localhost",user="root",password="Moulee009",autocommit=True)
            mycursor=connect.cursor()
            mycursor.execute("use bizcard")
            mycursor.execute(query)
            data_frame=display()
            st.write("""<h3><FONT COLOR='#32CD32>Datas are modifyed successfully..</h3>""",unsafe_allow_html=True)
            st.write("<h4>Successfully Updated...</h4>",unsafe_allow_html=True)
            st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
            st.dataframe(data_frame,hide_index=True)
    with tab3:
        st.markdown("<h3><FONT COLOR='#32527b'>Delete Datas</h3>",unsafe_allow_html=True)
        st.write("1. You can able to delete the values in the database")
        st.write("2. By providing the Email Id you can delete the entire row from the table")
        st.write("3. Or else you can able to delete all the values from the table")
        radio2=st.radio("Choose one option: ",options=["Delete row","Delete all"],key="radio2")
        if radio2=="Delete row":
            on = st.toggle('View Data',key="tog3")
            if on:
                data_frame=display()
                st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                st.dataframe(data_frame,hide_index=True)
            delete=st.text_input("Enter the Email Id:")
            if st.button("Delete",key="del10"):
                query=f"""delete from bizcard_datas where Email = '{delete}'"""
                connect= mysql.connector.connect(host="localhost",user="root",password="Moulee009",autocommit=True)
                mycursor=connect.cursor()
                mycursor.execute("use bizcard")
                mycursor.execute(query)
                data_frame=display()
                st.write("""<h3><FONT COLOR='#32CD32>Row is deleted successfully..</h3>""",unsafe_allow_html=True)
                st.write("<h4>Successfully Deleted one row...</h4>",unsafe_allow_html=True)
                st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                st.dataframe(data_frame,hide_index=True)
        if radio2=="Delete all":
            on = st.toggle('View Data',key="tog4")
            if on:
                data_frame=display()
                st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                st.dataframe(data_frame,hide_index=True)
            if st.button("Delete all",key="delete2"):
                query="truncate table bizcard_datas"
                connect= mysql.connector.connect(host="localhost",user="root",password="Moulee009",autocommit=True)
                mycursor=connect.cursor()
                mycursor.execute("use bizcard")
                mycursor.execute(query)
                data_frame=display()
                st.write("""<h3><FONT COLOR='#32CD32>All rows are deleted successfully..</h3>""",unsafe_allow_html=True)
                st.write("<h4>Successfully Deleted all the rows...</h4>",unsafe_allow_html=True)
                st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                st.dataframe(data_frame,hide_index=True)
if radio=="Choose path":
    st.markdown("<h3><FONT COLOR='#32527b'>Choose path</h3>",unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Insert", "Modify", "Delete"])
    with tab1:
        st.markdown("<h3><FONT COLOR='#32527b'>Insert Values</h3>",unsafe_allow_html=True)
        st.write("1. Store all the related images in a particular folder with '.png' or '.jpg'(That folder should contain only the business card related images)")
        st.write("2. Select the file path and paste it hereAfter selecting the image, Click the Submit button to perform the task")
        st.write("3. It will automatically displays all the images in that folder")
        st.write("4. From that you can select the image more than one at a time")
        st.write("""<h3><FONT COLOR='#32CD32>NOTE: Enter the correct path that images are stored</h3>""",unsafe_allow_html=True)
        on = st.toggle('View Data',key="tog5")
        if on:
            data_frame=display()
            st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
            st.dataframe(data_frame,hide_index=True)
        path=st.text_input("Enter the path that images are stored:")
        try:
            values=os.listdir(path)
            imas=[r for r in values if ".png" in r or ".jpg" in r or ".jpeg" in r]
            sel=st.multiselect("Select the image",imas,key="sel1")
            if st.button("Insert",key="btn2"):
                for im in sel:
                    img=cv2.imread(f"""{path}/{im}""")
                    result2=reader.readtext(img,detail=0)
                    final.append(result2)
                yes=filter_value(final)
                if yes:
                    st.write("""<h3><FONT COLOR='#32CD32>Successfully Inserted..</h3>""",unsafe_allow_html=True)
                    data_frame=display()
                    st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                    st.write("<h4>Successfully Inserted...</h4>",unsafe_allow_html=True)
                    st.dataframe(data_frame,hide_index=True)
        except:
            pass
    with tab2:
        st.markdown("<h3><FONT COLOR='#32527b'>Update Datas</h3>",unsafe_allow_html=True)
        st.write("1. You can able to change the values in the database")
        st.write("2. Enter the Email Id to modify the values")
        st.write("3. After given the email you have to specify the column name to modify")
        st.write("4. After specifying the column name enter the original data to change")
        on = st.toggle('View Data',key="tog6")
        if on:
            data_frame=display()
            st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
            st.dataframe(data_frame,hide_index=True)
        c1,c2,c3=st.columns(3)
        with c1:
            email=st.text_input("Enter the Email id: ")
        with c2:
            column=st.text_input("Enter the column name that you want to edit: ")
        with c3:
            value=st.text_input("Enter the data: ")
        if st.button("Modify"):
            query=f"""update bizcard_datas SET {column} = '{value}' WHERE Email = '{email}'"""
            connect= mysql.connector.connect(host="localhost",user="root",password="Moulee009",autocommit=True)
            mycursor=connect.cursor()
            mycursor.execute("use bizcard")
            mycursor.execute(query)
            data_frame=display()
            st.markdown("""<h3><FONT COLOR='#32CD32>Datas are modifyed successfully..</h3>""",unsafe_allow_html=True)
            st.write("<h4>Successfully Updated...</h4>",unsafe_allow_html=True)
            st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
            st.dataframe(data_frame,hide_index=True)
    with tab3:
        st.markdown("<h3><FONT COLOR='#32527b'>Delete Datas</h3>",unsafe_allow_html=True)
        st.write("1. You can able to delete the values in the database")
        st.write("2. By providing the Email Id you can delete the entire row from the table")
        st.write("3. Or else you can able to delete all the values from the table")
        radio2=st.radio("Choose one option: ",options=["Delete row","Delete all"],key="radio2")
        if radio2=="Delete row":
            on = st.toggle('View Data',key="tog7")
            if on:
                data_frame=display()
                st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                st.dataframe(data_frame,hide_index=True)
            delete=st.text_input("Enter the Email Id:")
            if st.button("Delete",key="del10"):
                query=f"""delete from bizcard_datas where Email = '{delete}'"""
                connect= mysql.connector.connect(host="localhost",user="root",password="Moulee009",autocommit=True)
                mycursor=connect.cursor()
                mycursor.execute("use bizcard")
                mycursor.execute(query)
                data_frame=display()
                st.write("""<h3><FONT COLOR='#32CD32>Row is deleted successfully..</h3>""",unsafe_allow_html=True)
                st.write("<h4>Successfully Deleted one row...</h4>",unsafe_allow_html=True)
                st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                st.dataframe(data_frame,hide_index=True)
        if radio2=="Delete all":
            on = st.toggle('View Data',key="tog8")
            if on:
                data_frame=display()
                st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                st.dataframe(data_frame,hide_index=True)
            if st.button("Delete all",key="delete2"):
                query="truncate table bizcard_datas"
                connect= mysql.connector.connect(host="localhost",user="root",password="Moulee009",autocommit=True)
                mycursor=connect.cursor()
                mycursor.execute("use bizcard")
                mycursor.execute(query)
                data_frame=display()
                st.write("""<h3><FONT COLOR='#32CD32>All rows are deleted successfully..</h3>""",unsafe_allow_html=True)
                st.write("<h4>Successfully Deleted all rows...</h4>",unsafe_allow_html=True)
                st.markdown("<h4>Bizcard Table</h3>",unsafe_allow_html=True)
                st.dataframe(data_frame,hide_index=True)
        
    