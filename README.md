# edgar-analytics-insight-coding-challenge

## I used python 3.5.4 to solve the coding challenge. 

### Only  sys, datetime, and os modules were used in the src/log_reporter.py

### To run the code, at the root directory of the repo, and run "./run.sh" in the terminal

### log_reporter.py is the code to process the provided log file line by line and write the session information into output file when the session is over

- The code process streaming data line by line, and no requirement of putting all data into memory. 
- Active sessions were stored in dictionary. ip is taken as key, and one Log_session object with all necessary information was the value.
- Together, I believe the code is fast and scalable. 

### Below are the details of the challenge

- './input/log.csv' file has ip, date, time, visited document details, etc. 
- './input/inactivity_period.txt' file has the value of valid session waiting time
- './output/sessionization.txt' file is the output from running log_reporter.py to include ip, session starting time, ending time, duration, and number of the visited documents. 


