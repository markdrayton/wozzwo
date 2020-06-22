# wozzwo

Parses whatsonzwift.com workout pages to produce `zwo` files for use in Zwift.

## Usage:

With Docker:

```bash
$ git clone https://github.com/markdrayton/wozzwo.git
$ cd wozzwo
$ docker build -t wozzwo .
$ docker run -it --rm wozzwo:latest "https://whatsonzwift.com/workouts/build-me-up/#id=week-11-breakfast-returns" > week-11-breakfast-returns.zwo
$ mv week-11-breakfast-returns.zwo ~/Documents/Zwift/Workouts/$ZWIFT_USER_ID
```

With `virtualenv`:

```bash
$ git clone https://github.com/markdrayton/wozzwo.git
$ pip3 install virtualenv
$ rehash
$ cd wozzwo
$ virtualenv venv --system-site-packages
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 wozzwo.py "https://whatsonzwift.com/workouts/build-me-up/#id=week-11-breakfast-returns" > week-11-breakfast-returns.zwo
$ mv week-11-breakfast-returns.zwo ~/Documents/Zwift/Workouts/$ZWIFT_USER_ID
$ deactivate
```
