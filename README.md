# Automatically Join Zoom Call Script
This is a python script that can be used to create shortcuts to automatically join your zoom lectures and save the hassle of having to navigate Canvas everytime to join your class. It includes the use of an online database so you can share meeting ids with your friends and classmates to streamline the process! The script is created utilizing python, selenium, docker, and sql. 

## Summary
Python script in order to create shortcuts to automatically join your zoom lectures.


## Commands

### python zoom.py -n/navi
Join your class based on the script navigating through your Canvas portal if you have not saved the class prior.
```
Username: (Put your username here)
Password: (Put your password here)

BUS-310-03-2208 - Introduction to Entrepreneurship
CPE-101-03-2208 - Fundamentals of Computer Science
CPE-315-05-2208 - Computer Architecture
MATH-244-01-2208 - Linear Analysis I

What class do you want to join? (input class name here) 

"Example: bus", this doesn't need full class name
```
### python zoom.py -h/help
Displays what commands you are able to use.
```
List of commands:
python zoom.py -n/navi
python zoom.py -h/help
python zoom.py -i/id
python zoom.py -j/join [classname/zoom_id]
python zoom.py -g/get [classname/zoom_id]
python zoom.py -a/add [classname] [zoom_id] [zoom_link]
python zoom.py -d/del [classname/zoom_id]
python zoom.py -s/show
```

### python zoom.py -s/show
Show all classes that you have previously saved.
```
1 | BUS-310-03-2208    | 1234567890 | www.linkedin.com
2 | MATH-244-01-2208   | 1234567891 | www.twitter.com
3 | CPE-101-03-2208    | 1234567892 | www.facebook.com
4 | CPE-315-05-LECTURE | 1234567893 | www.bing.com
5 | CPE-315-05-LAB     | 1234567894 | www.google.com
```

### python zoom.py -i/id
Join your zoom class based on the ID in the SQL Zoom table.
```
List of all classes: 
1 | BUS-310-03-2208
2 | MATH-244-01-2208
3 | CPE-101-03-2208
4 | CPE-315-05-LECTURE
5 | CPE-315-05-LAB
Input the SQL ID you want to join: (table number) Ex: 1
```

### python zoom.py -j/join [classname/zoom_id]
Input the classname or the zoom meeting id to join the zoom call.


### python zoom.py -g/get [classname/zoom_id]
Input your classname to get the respective zoom meeting id or input the zoom meeting id to get the name of the class.


### python zoom.py -a/add [classname] [zoom_id] [zoom_link]
Add an addition to the SQL Zoom table in order to save your class information.


### python zoom.py -d/del [classname/zoom_id]
Delete a class from the SQL Zoom table based on either the classname or zoom meeting id.


## Shortcut Creation

1) Create a new shortcut on your desktop screen

![Step One](https://i.imgur.com/Z0yrqNB.png)

2) Fill out the shortcut with the 'zoom.py' command of your choice after the '/c'

![Step Two](https://i.imgur.com/biH3H1g.png)

3) Stay organized and activate your shortcut whenever you have class!

![Step Three](https://i.imgur.com/xdO95Xq.png)
