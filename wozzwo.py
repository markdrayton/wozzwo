import argparse
import re
import sys
from enum import Enum

import requests
from lxml import etree, html
from lxml.builder import E

class StepPosition(Enum):
    FIRST = 0
    MIDDLE = 1
    LAST = 2

RAMP_RE = re.compile(
    r'(?:(?P<mins>\d+)min )?(?:(?P<secs>\d+)sec )?'
    r'(?:@ (?P<cadence>\d+)rpm, )?from (?P<low>\d+) to (?P<high>\d+)% FTP'
)

STEADY_RE = re.compile(
    r'(?:(?P<mins>\d+)min )?(?:(?P<secs>\d+)sec )?'
    r'@ (?:(?P<cadence>\d+)rpm, )?(?P<power>\d+)% FTP'
)

INTERVALS_RE = re.compile(
    r'(?P<reps>\d+)x (?:(?P<on_mins>\d+)min )?(?:(?P<on_secs>\d+)sec )?'
    r'@ (?:(?P<on_cadence>\d+)rpm, )?(?P<on_power>\d+)% FTP,'
    r'(?:(?P<off_mins>\d+)min )?(?:(?P<off_secs>\d+)sec )?'
    r'@ (?:(?P<off_cadence>\d+)rpm, )?(?P<off_power>\d+)% FTP'
)

FREE_RIDE_RE = re.compile(
    r'(?:(?P<mins>\d+)min )?(?:(?P<secs>\d+)sec )?free ride'
)

def calc_duration(mins, secs):
    d = 0
    if secs:
        d += int(secs)
    if mins:
        d += int(mins) * 60
    return d

def ramp(match, pos):
    label = {
        StepPosition.FIRST: "Warmup",
        StepPosition.LAST: "Cooldown"
    }.get(pos, "Ramp")
    duration = calc_duration(match["mins"], match["secs"])
    cadence = match.get("cadence")
    low_power = match["low"] / 100.0
    high_power = match["high"] / 100.0
    node = etree.Element(label)
    node.set("Duration", str(duration))
    node.set("PowerLow", str(low_power))
    node.set("PowerHigh", str(high_power))
    node.set("pace", str(0))
    if cadence:
        node.set("Cadence", str(cadence))
    return node

def steady(match, pos):
    duration = calc_duration(match["mins"], match["secs"])
    cadence = match.get("cadence")
    power = match["power"] / 100.0
    node = E.SteadyState(Duration=str(duration), Power=str(power), pace=str(0))
    if cadence:
        node.set("Cadence", str(cadence))
    return node

def intervals(match, pos):
    on_duration = calc_duration(match["on_mins"], match["on_secs"])
    off_duration = calc_duration(match["off_mins"], match["off_secs"])
    reps = match["reps"]
    on_power = match["on_power"] / 100.0
    off_power = match["off_power"] / 100.0
    on_cadence = match.get("on_cadence")
    off_cadence = match.get("off_cadence")
    node = E.IntervalsT(
        Repeat=str(reps),
        OnDuration=str(on_duration),
        OffDuration=str(off_duration),
        OnPower=str(on_power),
        OffPower=str(off_power),
        pace=str(0),
    )
    if on_cadence and off_cadence:
        node.set("Cadence", str(on_cadence))
        node.set("CadenceResting", str(off_cadence))
    return node

def free_ride(match, pos):
    # TODO: can have cadence?
    duration = calc_duration(match["mins"], match["secs"])
    return E.FreeRide(Duration=str(duration), FlatRoad=str(0))

BLOCKS = [
    (RAMP_RE, ramp),
    (STEADY_RE, steady),
    (INTERVALS_RE, intervals),
    (FREE_RIDE_RE, free_ride),
]

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="file or URL")
    return ap.parse_args()

def parse_node(step, pos):
    text = step.text_content()
    for regex, func in BLOCKS:
        match = regex.match(text)
        if match:
            match_int = {
                k: int(v) if v else None for k, v in match.groupdict().items()
            }
            return func(match_int, pos)
    raise RuntimeError(f"Couldn't parse {text}")

def fetch_url(url):
    return requests.get(url).content

def read_file(path):
    try:
        return open(path).read()
    except FileNotFoundError as e:
        return None

def text(tree, selector):
    return tree.xpath(f"{selector}/text()")[0]

def element_text(element, text):
    node = etree.Element(element)
    node.text = text
    return node

def main():
    args = parse_args()
    content = read_file(args.target)
    if not content:
        content = fetch_url(args.target)

    tree = html.fromstring(content)
    title = text(tree, '//h4[contains(@class, "flaticon-bike")]').strip()
    desc = text(tree, '//div[contains(@class, "workoutdescription")]/p')
    steps = tree.xpath('//div[contains(@class, "workoutlist")]/div')

    root = etree.Element("workout_file")
    root.append(element_text("author", "J. Doe"))
    root.append(element_text("name", title))
    root.append(element_text("description", desc))
    root.append(element_text("sportType", "bike"))
    root.append(etree.Element("tags"))
    workout = etree.Element("workout")

    for i, node in enumerate(steps):
        if i == 0:
            pos = StepPosition.FIRST
        elif i == len(steps) - 1:
            pos = StepPosition.LAST
        else:
            pos = StepPosition.MIDDLE
        workout.append(parse_node(node, pos))
    root.append(workout)

    etree.indent(root, space="    ")
    sys.stdout.write(
        etree.tostring(root, pretty_print=True, encoding="unicode"),
    )

if __name__ == "__main__":
    main()
