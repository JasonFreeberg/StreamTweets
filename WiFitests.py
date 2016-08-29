from WiFi import persistConnection, connected
import time
import subprocess

def dropConnection():
    print 'Fake network drop.'
    subprocess.call(['networksetup', '-setairportpower', 'en0', 'off'])

print '\n', '###########'
print 'First test.'
print '###########', '\n'



# TESTS

runs0 = 0
while runs0 <= 20:
    if runs0 == 3:
        dropConnection()
    if runs0 == 5:
        print 'Fake re-establish'
        subprocess.call(['networksetup', '-setairportpower', 'en0', 'on'])
    connected()
    runs0 += 1
    time.sleep(0.5)

print '\n', '###########'
print 'Next test.'
print '###########', '\n'

runs = 0
while persistConnection():
    if runs == 3:
        dropConnection()
    runs += 1
    time.sleep(0.5)
    if runs == 25:
        break

print '\n', '###########'
print 'Manual test.'
print '###########', '\n'

while persistConnection():
    time.sleep(0.5)
