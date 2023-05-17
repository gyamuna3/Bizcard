# Bizcard Extracting_Business Card Data with OCR 
EasyOCR, as the name suggests, is a Python package that allows computer vision developers to effortlessly perform Optical Character Recognition.It is a Python library for Optical Character Recognition (OCR) that allows you to easily extract text from images and scanned documents. In my project I am using easyOCR to extract text from business cards.
      The EasyOCR package can be installed with a single pip command.
      The dependencies on the EasyOCR package are minimal, making it easy to configure your OCR development environment.
      Once EasyOCR is installed, only one import statement is required to import the package into your project.
      From there, all you need is two lines of code to perform OCR — one to initialize the Reader class and then another to OCR the image via the readtext function.
A webpage is displayed in browser, I have created the app with three menu options namely  UPLOAD , VIEW, MODIFY  and DELETE where user has the option to upload the respective Business Card whose information has to be extracted, stored, modified or deleted if needed.

Once user uploads a business card, the text present in the card is extracted by easyocr library.

The extracted text is sent to load model() function for respective text classification as company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code.

On Clicking Insert into SQL Database Button the data gets stored in the MySQL Database. 

Further with the help of VIEW,UPDATE and DELETE menu the uploaded data’s in SQL Database can be accessed for Read, Update and Delete Operations.
