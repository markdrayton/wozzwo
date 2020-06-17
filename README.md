# wozzwo

Parses whatsonzwift.com workout pages to produce `zwo` files for use in Zwift.

## Usage:

With Docker:

```bash
$ docker build -t wozzwo .
$ docker run -it --rm wozzwo:latest "https://whatsonzwift.com/workouts/build-me-up/#id=week-11-breakfast-returns" > week-11-breakfast-returns.zwo
$ mv week-11-breakfast-returns.zwo ~/Documents/Zwift/Workouts/$ZWIFT_USER_ID
```

Without:

```bash
$ pip3 install -r requirements.txt
$ python3 wozzwo.py "https://whatsonzwift.com/workouts/build-me-up/#id=week-11-breakfast-returns" > week-11-breakfast-returns.zwo
$ mv week-11-breakfast-returns.zwo ~/Documents/Zwift/Workouts/$ZWIFT_USER_ID
```
