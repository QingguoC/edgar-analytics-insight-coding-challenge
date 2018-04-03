# edgar-analytics-insight-coding-challenge

## I used python 3.5.4 to solve the coding challenge under Ubuntu 14.04 system. 

### The code is all in src/log_reporter.py with only sys, datetime, and os modules used. 

### To run the code, at the root directory of the repo, run "./run.sh" in the terminal

### log_reporter.py is the code to process the provided log file line by line and write the session information into output file when the session is over

- The code processes streaming data line by line, and there is no requirement of putting all data into memory. 
- Active sessions are stored in dictionary. ip is taken as key, and one Log_session object with all necessary information is the value.
- Together, I believe the code is fast and scalable. 

### Below are some other details of the challenge

- './input/log.csv' file has ip, date, time, visited document details, etc. 
- './input/inactivity_period.txt' file has the value of valid session waiting time
- './output/sessionization.txt' file is the output from running log_reporter.py to include ip, session starting time, ending time, duration, and number of the visited documents. 


