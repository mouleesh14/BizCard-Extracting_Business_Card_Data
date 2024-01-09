# BizCard-Extracting_Business_Card_Data
The aim of the project is to built a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information would include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pincode. The extracted information would then be displayed in the application's graphical user interface (GUI).

The application would also allow users to save the extracted information into a MYSQL database along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information.

# Approach:
1. Implement image processing and OCR
2. Implement database integration
3. Display the extracted information

# OCR (Optical Character Recognition):
OCR is a technology that converts different types of documents, such as scanned paper documents, PDFs, or images captured by a digital camera, into editable and searchable data. OCR software analyzes the shapes and patterns of text in a document and translates it into machine-encoded text. The primary purpose of OCR is to extract text from physical or digital documents so that it can be edited, searched, stored more efficiently, or used in other applications.

# Easy OCR: 
It's a software or services that are user-friendly and designed to simplify the process of extracting text from images or scanned documents. These tools are often equipped with intuitive interfaces, making them accessible to users with varying levels of technical expertise. users typically upload or input an image or document, and the software automatically performs the optical character recognition, providing editable and searchable text as the output. 

# OpenCV:
OpenCV (Open Source Computer Vision) is a popular open-source library for computer vision and image processing tasks. OpenCV provides a comprehensive set of tools and functions that enable developers to work with images and videos efficiently. Its versatility makes it suitable for a wide range of applications, from basic image manipulation to complex computer vision tasks. 

Some key features of OpenCV include image and video input/output, image processing and manipulation, feature detection and matching, object recognition, camera calibration, and machine learning. It supports a variety of image formats and can handle real-time processing, making it a valuable tool for applications like robotics, augmented reality, and facial recognition.

# Implement Database:
Use a database management system like SQLite or MySQL to store the extracted information along with the uploaded business card image. You can use SQL queries to create tables, insert data, and retrieve data from the database, Update the data and Allow the user to delete the data. Improve the application by adding new features, optimizing the code, and fixing bugs. You can also add user authentication and authorization to make the application more secure.

# Visulaization:
Create a simple and intuitive user interface using Streamlit that guides users through the process of uploading the business card image and extracting its information. You can use widgets like file uploader, buttons, and text boxes to make the interface more interactive. GUI development, and database management. It would also require careful design and planning of the application architecture to ensure that it is scalable, maintainable, and extensible. Good documentation and code organization would also be important for the project.

# Tools:
1. Python
2. MYSQL workbench
3. OCR, cv2
4. Streamlit

# Requried Libaries:
1. Easy ocr
2. pandas
3. PIL, Image
4. Regular expression
5. cv2
6. mysql.connector
