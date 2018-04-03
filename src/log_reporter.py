#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 16:52:29 2018

@author: qingguo
"""

import sys
from datetime import datetime as dt
import os

#format string to timestamp
def convert_str_to_timestamp(time_str):
    return dt.strptime(time_str,'%Y-%m-%d %H:%M:%S').timestamp()
    
#format timestamp to string   
def convert_timestamp_to_str(timestamp):
    return dt.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# append batch expired sessions into file    
def write(batch,output_file):
    has_file = os.path.isfile(output_file) and os.path.getsize(output_file) > 0
    with open(output_file,'a') as f:     
        for i, log_session in enumerate(batch):
            st_time = convert_timestamp_to_str(log_session.start_time)
            ed_time = convert_timestamp_to_str(log_session.last_time)
            duration = str(int(log_session.last_time - log_session.start_time + 1))
            log_summary = ",".join([log_session.ip,st_time,ed_time,duration,str(log_session.count)])
            if not has_file and i == 0:
                f.write(log_summary)
            else:
                f.write("\n"+log_summary)
                

# read the inactivity_period 
def load_inactivity_period(inactivity_period_file):
    inactivity_period = 0
    with open(inactivity_period_file) as f:
        inactivity_period = int(f.readline().replace(",","").strip())
    return inactivity_period   

# store necessary in one class         
class Log_session():
    def __init__(self,ip,start_time, last_time,count,log_id):
        self.ip = ip
        self.start_time = start_time
        self.last_time = last_time
        self.count = count
        self.log_id = log_id

# main function to read and write log stats
def main(log_file,inactivity_period_file,output_file):
    
    # intialize inactivity_period
    inactivity_period = load_inactivity_period(inactivity_period_file)
    
    curr_time = None  # track current time by second
    second_batch = [] # the batch records waiting to be written in same second
    session_dict = {} # active session record dictionary
    expired_session = [] # expired session list waiting to be deleted from session_dict
    with open(log_file,'r') as f:
        # loop for reading data row by row with index
        for i, row in enumerate(f):
            if row and row[0] != 'i': # check if not header
                row_elements = row.split(',')
                
                if not curr_time: # first record
                    curr_time = convert_str_to_timestamp(row_elements[1] + ' ' + row_elements[2])
                    session_dict[row_elements[0]] = Log_session(row_elements[0],curr_time,curr_time,1,i)
                else:
                    row_time = convert_str_to_timestamp(row_elements[1] + ' ' + row_elements[2])    
                    if row_time != curr_time: # then it is time to check expiration of session, and write the stats into file
                        curr_time = row_time
                        for ip in session_dict:
                            if curr_time - session_dict[ip].last_time > inactivity_period:
                                second_batch.append(session_dict[ip])
                                expired_session.append(ip)
                        for ip in expired_session:
                            del session_dict[ip]
                        expired_session = []
                        
                        if len(second_batch) > 0:
                            #print("writing")
                            second_batch.sort(key=lambda x: x.log_id) # sort the list by the row index before write
                            write(second_batch, output_file)
                            second_batch = []
                            
                    if row_elements[0] not in session_dict:
                        session_dict[row_elements[0]] = Log_session(row_elements[0],row_time,row_time,1,i)
                    else:
                        old_session = session_dict[row_elements[0]]
                        if row_time - old_session.last_time > inactivity_period:
                            second_batch.append(old_session)
                            new_session = Log_session(row_elements[0],row_time,row_time,1,i)
                            session_dict[row_elements[0]] = new_session
                        else:
                            old_session.last_time = row_time
                            old_session.count += 1                    

    for ip in session_dict:      
        second_batch.append(session_dict[ip])

    if len(second_batch) > 0:
        second_batch.sort(key=lambda x: x.log_id)
        write(second_batch, output_file) 

if __name__ == '__main__':
    if len(sys.argv) < 4 or (not os.path.isfile(sys.argv[1])) or (not os.path.isfile(sys.argv[2])):
        print("Syntax is 'python log_reporter.py log_file inactivity_period_file output_file'")
        print("make sure the files exist")
    else:
        log_file = sys.argv[1]
        inactivity_period_file = sys.argv[2]
        output_file = sys.argv[3]
        try:
            main(log_file,inactivity_period_file,output_file)
        except Exception as e:
            print(e)
            print("Syntax is 'python log_reporter.py log_file inactivity_period_file output_file'")
