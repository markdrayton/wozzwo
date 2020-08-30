import argparse
import sys

from lxml import etree

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("ftp", type=int)
    ap.add_argument("path")
    return ap.parse_args()

def parse_ramp(elem):
    dur = int(elem.attrib["Duration"])
    start = float(elem.attrib["PowerLow"])
    end = float(elem.attrib["PowerHigh"])
    diff = end - start
    return [start + (diff * (d / dur)) for d in range(dur)]

def parse_steadystate(elem):
    return int(elem.attrib["Duration"]) * [float(elem.attrib["Power"])]

def parse_intervals(elem):
    out = []
    for _ in range(int(elem.attrib["Repeat"])):
        out.extend(int(elem.attrib["OnDuration"]) * [float(elem.attrib["OnPower"])])
        out.extend(int(elem.attrib["OffDuration"]) * [float(elem.attrib["OffPower"])])
    return out

TAGS = {
    "Warmup": parse_ramp,
    "SteadyState": parse_steadystate,
    "IntervalsT": parse_intervals,
    "Ramp": parse_ramp,
    "Cooldown": parse_ramp,
}

def avg(l):
    return sum(l) / float(len(l))

def fmt_duration(s):
    hours = s // 3600
    mins = (s % 3600) // 60
    secs = s % 60
    return f"{hours:d}h{mins:d}m{secs:d}s"

def main():
    args = parse_args()
    points = []
    for action, elem in etree.iterparse(args.path):
        fn = TAGS.get(elem.tag)
        if fn:
            points.extend(fn(elem))
    duration = len(points)

    if duration < 30:
        print("Workout duration must be at least 30s", file=sys.stderr)
        sys.exit(1)

    raised = []
    for start in range(duration - 30):
        end = start + 30
        raised.append(avg(points[start:end]) ** 4)

    np = (avg(raised) ** 0.25) * args.ftp
    intensity = np / args.ftp
    tss = ((duration * np * intensity) / (args.ftp * 3600)) * 100

    print(f"{fmt_duration(duration)} np {np:.0f} if {intensity:.2f} tss {tss:.0f}")

if __name__ == "__main__":
    main()
