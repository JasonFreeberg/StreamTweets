# StreamTweets
A python script that streams Tweets filtered by keyword, location, both, or none. Also includes a "WiFi" module that will reconnect your WiFi if you wish to stream 24/7. I made this so the newer members of Data Science at UCSB can speed up the data-wrangling phase and get into the more fun parts of a data-driven project.

main.py takes a text file as a command line argument. Refer to "mockFile.txt" for a reference. This text file should contain your...
- Twitter App key
- secret
- access token
- access secret code
- MongoDB Database name
- Collection name within that database
- Location of the MongoDB's data

WiFi.py contains two functions: connected() and persistConnection().
connected() will ping Google's static dialup IP address, 8.8.8.8, to check for a connection. Returns True if the connection is fine, returns False otherwise.
persistConnection() calls connected(). If the connection is bad, the function will turn your WiFi off and on, wait, then call connected again. The process continues until the connection is made or wait limit is reached. Waiting time between connection attempts grows exponentially.