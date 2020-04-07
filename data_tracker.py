import argparse
from cov19 import Cov19Statistics, __version__
from cov19.collect import Austria, Germany, Switzerland, UnitedKingdom, UnitedStates


parser = argparse.ArgumentParser(description="Program which tracks the SARS-Cov-2 infection rate in "
                                             "Germany, Austria, Switzerland, United Kingdom, United States")
parser.add_argument("--version", action='version', version=__version__)
parser.add_argument("log_file", default="cov19_stats.log", help="the file to log statistics into", type=str)
args = parser.parse_args()

cov19 = Cov19Statistics(args.log_file)
for country in [Germany, Austria, Switzerland, UnitedKingdom, UnitedStates]:
    c = country()
    cov19.add_country(c)

cov19.run()
