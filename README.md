# BlueHub_GUI
NCKU course crawler.

## Version
### **`2.1`**
Afer the NCKU course web had been upgrated, the original version of BlueHub couldn't work any more. I tried to use basic get/post methods to get the information of web, but it's difficult because the form-data was encrypted. So I use [**selenium**](https://www.selenium.dev/documentation/en/)--- a slower, but more powerful tool to get what I want. It probably takes 10 seconds to obtain the html of web.

## Features
* Search the course information.
* Schedule the searching list.
* Send email to notify the user when the course is not full.
* Use Tor routing to change IP every time.
* Show current IP.

## Demo
* Logging picture

![GUI1](./image/logging.PNG)

(cover picture refers from [openclipart.org](https://openclipart.org/image/400px/svg_to_png/319171/ladybookandglobe-1901.png))

* Menu

![GUI2](./image/menu.PNG)

## Future
* Use line-bot or messenger-bot to take the place of email.
* Beautify GUI.

## Notification
* When using the email-sending function, you need open the permission of third-party sites & apps requests.
* Using different IDE to excute this program may lead to a little different layout of GUI.(Demo picture is using spyder)

## Declaration
* This project is **only for education purpose**.
* Documents specified above follow the rules of separate authorization regulations.
