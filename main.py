import argparse
import dataclasses
import datetime

import dateutil.parser
import pytz

tz = pytz.timezone("US/Pacific")
bsize = 1_000
fudge = bsize**2 / 18
max = 5.99 * 10**9
remaining = 3.12 * 10**9
remaining = max - 3.17 * 10**9
remaining = 3.06 * 10**9
used = max - remaining


@dataclasses.dataclass
class MyThing:
    end_date = dateutil.parser.parse("12/2/2022").astimezone(tz)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--xls",
    action="store_true",
    default=False,
    help="output for xls",
    required=False,
)
args = parser.parse_args()

output_format = "xls" if args.xls else "console"


def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
    sample code:
        print('mb= ' + str(bytesto(314575262000000, 'm')))

    sample output:
        mb= 300002347.946
    """

    a = {"k": 1, "m": 2, "g": 3, "t": 4, "p": 5, "e": 6}
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return r


def format_output(days_counter, diff, used, remaining, format=output_format):
    gb1 = bytesto(used, "g", bsize=bsize)
    gb2 = bytesto(remaining, "g", bsize=bsize)

    if not format == "console":
        return f"{(start_date + diff).date()}\t{mb2}\t{gb1}\t{gb2}"
    return f"{(start_date + diff).date()} {mb2:,.2f} {gb1:,.2f}GB {gb2:,.2f}GB"


start_date = datetime.datetime.now(tz)

mt = MyThing()

diff = mt.end_date - start_date
diff = mt.end_date - start_date + datetime.timedelta(days=1)
per_day = remaining / diff.days + fudge

mb2 = bytesto(per_day, "m", bsize=bsize)

days_counter = 0
diff = datetime.timedelta(days=days_counter)
while start_date + diff <= mt.end_date:
    diff = datetime.timedelta(days=days_counter)
    out = format_output(
        days_counter, diff, used=used, remaining=remaining, format=output_format
    )
    print(out)
    days_counter += 1
    used += per_day
    remaining = max - used

print(f"from {start_date.date()} to {mt.end_date.date()} is {diff.days} days")
