# RestaurantManagementSystem

Restaurant Management System built using PyQt5 GUI

## Application Requirement

- Make sure you have python installed in your machine.
- Install PyQt5
- Install mysql client (mysql.connector)

## Running the Application

- Clone the project
- cd rms
- type python **main**.py in terminal

### Preview

![Alt text](screenshots/01.png)<br/>
![Alt text](screenshots/02.png)<br/>
![Alt text](screenshots/03.png)<br/>
![Alt text](screenshots/04.png)<br/>
![Alt text](screenshots/05.png)<br/>
![Alt text](screenshots/06.png)<br/>
![Alt text](screenshots/07.png)<br/>

## How to Run dev

`python3 -m venv venv`

In Windows

`. .\venv\Scripts\activate`

In Linux

`source venv/bin/activate`

### Install packages

`pip install -r requirements.txt`

### Package it into exe

`pyinstaller --onefile --noconsole __main__.py`

### Generate requirement.txt

`pip3 freeze > requirements.txt`
