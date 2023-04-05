#!/bin/bash

# Stop cryptosimpir service
sudo systemctl stop cryptosimpir
# Stop pirweb service
sudo systemctl stop pirweb

# Kill mono, dotnet and LOGCACHE processes
sudo pkill -f -9 mono
sudo pkill -f -9 dotnet
sudo pkill -f -9 LOGCACHE

# Connect to MySQL and truncate tables
sudo mysql -u(username) -p -e "use cryptosimpir; truncate pir_jobs; truncate pir_jobcancelrequests; truncate pir_currentmasters; truncate pir_currentmasterscandidates;"

# Start pirweb and cryptosimpir services
sudo systemctl start pirweb
sudo systemctl start cryptosimpir

