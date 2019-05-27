# Udacity Item Catalog project: -
### By Ahmed Alhawsawi
## ReadMe.md 

### Introduction
This project is the second project for those who enrolled in Full-Stack Web Developer Nanodegree program which is introduced by Udacity platform. The aim of this project is to build the website that combined the skills of building database, working with CRUD, and python with the integration of third party as authentication and authorization. 
The aim of this project is to build the website that combine the all skills that the
### Requirements:  
•	Python 2.7, 3.5 or latest version of Python programming language.
•	VartualBox the software that runs the Virtual Machine (VM) environment locally in the Operating System (OS).
•	Vagrant the software that lunches and configures the virtual machine in your computer.
•	Git a free and open source Unix-style terminal.

### Requirements:  

- [Python 3.6.7](www.python.org) – or latest version of Python programming language.
- [VartualBox](www.vartualbox.org/wiki/Downloads) the software that runs the Virtual Machine (VM) environment locally in the Operating System (OS).
- [Vagrant](www.vagrantup.com) – the software that lunches and configures the virtual machine in your computer.
- [Git](www.git-scm.com) – a free and open source Unix-style terminal. 

### How to get to the project: 
Downloading VartualBox and Vagrant from their websites and setting all the requirements for the virtual machine. 

Downloading [VartualBox](www.vartualbox.org/wiki/Downloads) and from the website
[VartualBox](www.vartualbox.org/wiki/Downloads) software will be installed to the OS firstly. Next, the installation of [vagrant](www.vagrantup.com) will take place. After the installation of these two software the work will be on command line to run the virtual machine and configure its all settings.  

### Runing the virtual machine
- vagrant up
- vagrant ssh
- cd  /vagrant/catalog 
- python database_setup.py
- python lotofmenu.py
- python application.py
- Then Accessing and testing the application by visiting http://localhost:8000 locally

### Project Structure: 
'''
.
+-- application.py
+-- client_secrets.json
+-- database_setup.py
+-- lotofmenu.py
+-- README.md
+-- static
¦   +-- style.css
+-- templates
    +-- car.html
    +-- deletecar.html
    +-- deleteitem.html
    +-- editcar.html
    +-- edititem.html
    +-- header.html
    +-- main.html
    +-- login.html
    +-- menu.html
    +-- menuitem.html
    +-- newcar.html
    +-- newcaritem.html
    +-- publiccar.html
    +-- publiccaritem.html
	'''



