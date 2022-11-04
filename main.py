import argparse
import datetime

import dateutil.parser
import pytz

parser = argparse.ArgumentParser()
parser.add_argument(
    "--xls",
    action="store_true",
    default=False,
    help="output for xls",
    required=False,
)
args = parser.parse_args()


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


def format_output(days_counter, diff, used, remaining, format="console"):
    gb1 = bytesto(used, "g", bsize=bsize)
    gb2 = bytesto(remaining, "g", bsize=bsize)

    if not format == "console":
        return f"{(now + diff).date()}\t{mb2}\t{gb1}\t{gb2}"
    return f"{(now + diff).date()} {mb2:,.2f} {gb1:,.2f}GB {gb2:,.2f}GB"


tz = pytz.timezone("US/Pacific")

datestamp = "12/2/2022"

end_date = dateutil.parser.parse(datestamp).astimezone(tz)

now = datetime.datetime.now(tz)

diff = end_date - now
diff = end_date - now + datetime.timedelta(days=1)

max = 6 * 10**9
remaining = 3.12 * 10**9
remaining = max - 3.17 * 10**9
bsize = 1_000
used = max - remaining
fudge = bsize**2 / 18
per_day = remaining / diff.days + fudge

mb2 = bytesto(per_day, "m", bsize=bsize)

i = 0
diff = datetime.timedelta(days=i)

days_counter = 0
while now + diff <= end_date:
    diff = datetime.timedelta(days=days_counter)
    out = format_output(
        days_counter, diff, used=used, remaining=remaining, format="console"
    )
    print(out)
    days_counter += 1
    used += per_day
    remaining = max - used

print(f"from {now.date()} to {end_date.date()} is {diff.days} days")
