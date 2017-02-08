How to install Overwatch Match Tracker:

Installing Python:
You first need to install Python 3.4 on your machine in order to run Python code.
Follow this guide here to install ---> http://www.howtogeek.com/197947/how-to-install-python-on-windows/

Once you have Python installed, open the Overwatch Match Tracker folder and edit the "login.txt" file as follows:
There are two lines username and password. Edit each line so that it reads: username=YourUsername followed by password=YourPassword
Make sure each is on its own line and that there are no spaces.
Save it and close it.

In order for your username and password to work on the database, I must add them to the whitelist.
So when you are ready, let me know to add it.

Lastly, you need to create a shortcut to run the script.
Right click the file called "main.py" and select "Create Shortcut".
Right click the shortcut file and select Properties. Under Target, add the file path for python.exe before the file path currently displayed as the Target. Example:
Before: Target: C:\OverwatchMatchTracker\main.py --> After: Target: C:\Users\Python34\python.exe C:\OverwatchMatchTracker\main.py
Click Apply and then OK.

Now you can run the application from the newly created shortcut.