yelpProject
===========

Final Project Fall 2014

Create a credentials.py file and save to working directory. The file should look like this:
```
# credentials.py
mongo = {
    'user': 'username',
    'secret': 'secret',
    'url': 'oceanic.mongohq.com:10018/playground'
}
```
where username and secret were emailed to you. Keep the url exactly as shown.

Possible Improvements
=====================

In onboard_user.py line 19, may want to cast numerator and denominator of division to floats. This gives better granularity for categorical ratings. May want to cast all stars of type float for consistency.