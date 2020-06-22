# wozzwo

Parses whatsonzwift.com workout pages to produce `zwo` files for use in Zwift. Note that the resulting workouts don't include the text messages that in-game workouts include because they aren't listed on whatsonzwift.com.

## Usage

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

## Example output

```bash
$ wozzwo https://whatsonzwift.com/workouts/build-me-up/week-10-serrated/
<workout_file>
    <author>J. Doe</author>
    <name>Serrated</name>
    <description>Intervals that come up to a very sharp point, looking like a serrated knife upon post-workout review. This workout will make you sharp for race day, ready to tackle the surges of terrain and competition.</description>
    <sportType>bike</sportType>
    <tags/>
    <workout>
        <Warmup Duration="300" PowerLow="0.4" PowerHigh="0.65" pace="0"/>
        <SteadyState Duration="300" Power="0.65" pace="0" Cadence="95"/>
        <SteadyState Duration="180" Power="0.8" pace="0" Cadence="100"/>
        <SteadyState Duration="120" Power="0.55" pace="0" Cadence="85"/>
        <Ramp Duration="120" PowerLow="1.1" PowerHigh="1.3" pace="0"/>
        <SteadyState Duration="120" Power="0.55" pace="0" Cadence="85"/>
        <Ramp Duration="120" PowerLow="1.1" PowerHigh="1.3" pace="0"/>
        <SteadyState Duration="120" Power="0.55" pace="0" Cadence="85"/>
        <Ramp Duration="120" PowerLow="1.1" PowerHigh="1.3" pace="0"/>
        <SteadyState Duration="120" Power="0.55" pace="0" Cadence="85"/>
        <Ramp Duration="120" PowerLow="1.1" PowerHigh="1.3" pace="0"/>
        <SteadyState Duration="120" Power="0.55" pace="0" Cadence="85"/>
        <Ramp Duration="120" PowerLow="1.1" PowerHigh="1.3" pace="0"/>
        <SteadyState Duration="120" Power="0.55" pace="0" Cadence="85"/>
        <Ramp Duration="120" PowerLow="1.1" PowerHigh="1.3" pace="0"/>
        <SteadyState Duration="480" Power="0.55" pace="0" Cadence="85"/>
        <Ramp Duration="30" PowerLow="1.3" PowerHigh="1.5" pace="0"/>
        <IntervalsT Repeat="5" OnDuration="180" OffDuration="60" OnPower="0.88" OffPower="1.0" pace="0" Cadence="90" CadenceResting="90"/>
        <Ramp Duration="30" PowerLow="1.3" PowerHigh="1.5" pace="0"/>
        <IntervalsT Repeat="5" OnDuration="180" OffDuration="60" OnPower="0.88" OffPower="1.0" pace="0" Cadence="90" CadenceResting="90"/>
        <SteadyState Duration="240" Power="0.45" pace="0"/>
    </workout>
</workout_file>
```
