#!/usr/bin/env python3
### Copyright: NOKIA 2023
### Author: Sergio Chavez sergio.chavez_cardenas@nokia.com

from scrapli import Scrapli
import time
import re
import sys
import argparse
import math
import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


    
def sros_cmd(cmd,**router):
    with Scrapli(**router) as conn:
        conn.open()
        print("Sending command \'%s\' to %s host %s:" % (cmd,router["platform"],router["host"]))
        response = conn.send_command(cmd)
        return response.result   
    
def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    sys.stdout.flush()

def push_to_prometheus(data=None,gw="localhost:9091", jobName="MyJob1"):
    registry = CollectorRegistry()
    for component, metrics in data.items():
       for key, value in metrics.items():
         # Create a gauge metric for each key in the data
         g = Gauge(f'{component}_{key}', f'Description of {component}_{key}', registry=registry)
         # Set the value of the gauge
         g.set(value)
    push_to_gateway(gw, job=jobName, registry=registry)
   
def show_card_virtual_fp(**router):
    with Scrapli(**router) as conn:
       conn.open()
       start_time = time.time()
       while True: 
          time.sleep(5)
          response = conn.send_command("/show card 1 virtual fp | match %")
          lines = response.result.strip().split('\n')    
          parsed_data = {}
          #PARSE OUTPUT
          for line in lines:
              # Split each line into parts
              parts = line.split()
              # The first part is the name, the rest are the values
              # Replace is used to convert some string that come with the "+" signs
              name = parts[0].replace("+", "_")
              numeric_parts = [item for item in parts[1:] if item.replace('.', '', 1).isdigit()]
              values = {f"key{i}": float(value) for i, value in enumerate(numeric_parts, 1)}
              # Store in the dictionary
              # print(values)
              parsed_data[name] = values
          print(parsed_data)
          #PUSH GATEWAY
          push_to_prometheus(data=parsed_data,gw="localhost:9091",jobName=router["host"])

def sros_check_fib_output(expected=None,timeout_s=900, **router):
    with Scrapli(**router) as conn:
       conn.open()
       start_time = time.time()
       #timeout_s= 900 # 15 minutes
       end_time = start_time + timeout_s  
       nr_of_routes = "0"
       # cmd="/tools dump router fib 1 summary | match Total"
       cmd="show router fib 1 summary | match Total"
       print("Sending \'%s\' command to %s host %s:" % (cmd,router["platform"],router["host"]))
       while time.time() < end_time:
           response = conn.send_command(cmd)
           execution_time = time.time() - start_time
           if "Total Installed" in response.result:
              nr_of_routes = re.findall(r'\d+', response.result)[0]
              if expected == None:
                 break
              else: 
                if nr_of_routes != expected:
                    time.sleep(1)
                    progress_bar(math.ceil(execution_time), timeout_s, prefix="Progress: {}/{}".format(nr_of_routes,expected), suffix="Time: {:.1f}/{}s".format(execution_time,timeout_s) , length=50)
                else: 
                    break
           else: 
              time.sleep(1)
              progress_bar(math.ceil(execution_time), timeout_s, prefix="Progress: {}/{}".format(nr_of_routes,expected), suffix="Time: {:.1f}/{}s".format(execution_time,timeout_s) , length=50)
              
       print("\nTotal Execution time: %.2fs" % execution_time)
       print("Total Routes: %s" % nr_of_routes)
       return nr_of_routes

def main():
    parser = argparse.ArgumentParser(description='A script that performs a clear fib on a router to check convergence')
    parser.add_argument('host',metavar="IP", help='The IP of the host argument')
    parser.add_argument('-u','--username', dest="username", default="admin", help='The username of the host')
    parser.add_argument('-p','--password', dest="password", default="admin", help='The username of the host')
    parser.add_argument('-P','--platform', dest="platform", default="nokia_sros",help='The platform of the host')
    parser.add_argument('-t','--timeout', dest="timeout", default=900, type=float ,help='Convergence timeout in seconds')
    parser.add_argument('-v','--variant', dest="variant", default=None,help='The variant for Scrapli parser. Use in cases like "classic" SROS')
    args = parser.parse_args()
    ## Define variable for connecting to host using SSH (via Scrapli)
    target= {
        "host" : args.host,
        "auth_username": args.username,
        "auth_password": args.password,
        "auth_strict_key": False,
        "platform": args.platform,
        "variant": args.variant,
    }
    fp = show_card_virtual_fp(**target)
  

if __name__ == "__main__":
    main()   