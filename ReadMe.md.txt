
# Udacity Logs Analysis project:-
### By Ahmed Alhawsawi
## ReadMe.md 

## Table of contents 
### introduction
This project is for those who enrolled in Full-Stack Web Developer Nanodegree program which is provided by Udacity platform. The aim of this project is to improve the skills of the trainees in SQL database server by working with data that have millions of rows. To achieve the project’s goals, there are some requirements to be met and procedures to be followed. 
### Requirements:  

- [Python 3.6.7](www.python.org) – or latest version of Python programming language.
- [VartualBox](www.vartualbox.org/wiki/Downloads) the software that runs the Virtual Machine (VM) environment locally in the Operating System (OS).
- [Vagrant](www.vagrantup.com) – the software that lunches and configures the virtual machine in your computer.
- [Git](www.git-scm.com) – a free and open source Unix-style terminal. 

### How to git to the project: 
[VartualBox](www.vartualbox.org/wiki/Downloads) software will be installed to the OS firstly. Next, the installation of [vagrant](www.vagrantup.com) will take place. After the installation of these two software the work will be on command line to run the virtual machine and configure its all settings.  
A **_vagrantfile_** is a file that can be used to initiate the system by using vagrant program. This file contains all other neccessary files and tools for this project. This is provided by Udacity platform.

Running a _vagrantfile_ with **vagrant up** command will install Ubuntu Linux OS and setup all the other settings that required for this project.
If the setup is done successfully, then the use of **_Vagrant ssh_** command will take place to log in to the system. 
In case of any failure of logging to the system after executing this command, **winpty vagrant ssh** command can be used instead to log in to the system. If this command doesn’t work either, running **vagarnt up**command again can solve this problem. In case of the operation unsolved the problem, the installation of different version of vagrant can be one solution of it.

If the system is working properly, PostgreSQL database server will start inside the VM. Then _psql_ command will be used to access and run SQL statements.

### Runing the virtual machine
These steps will be taken after successful setup:
- cd  /vagrant to change the dircotory to access the main files.
- **Vagrant ssh**
- In case if **vagrant ssh** not working – **winpty vagrant ssh**
-	**psql – d news – f newsdata.sql**: connecting with news data base and loading newsdata.sql file to the VM.
-	**\lc or psql –d news** to connect db. 
-	**\dt**  list all tables
-	**\d** table_name to llist columns and rows in assigned table

### create Views:
For question 3 in logs analysis project:

**Q_3:On which days did more than 1% of requests lead to errors?**
```
create view Days_Rate as
	 select time:date as day, count(*) as num 
	 from log 
	 group by day;
	 
create view Error_Rate as
     select time::date as day, count(*) as num
	 from log 
	 where status like '404%'
	 group by day 
	 order by day;
	 
create view All_Rate as	
	 select Days_Rate.day, Days_Rate.num as Rate, Error_Rate.num as Error
	 from Days_Rate, Error_Rate
	 where Days_Rate.day = Error_Rate.day
	 group by Days_Rate.day, Days_Rate.num, Error_Rate.num; 
```


