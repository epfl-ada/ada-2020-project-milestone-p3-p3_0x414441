## !pip install gtab
import gtab
import pandas as pd
import pickle
import os

TERROR_FILE = 'google_terrorism.obj'
TIMEFRAME = '2011-01-01 2015-12-31'
ANCHORBANK = 'google_anchorbank_geo=_timeframe=' + TIMEFRAME + '.tsv'
GTAB_DIR = './gtab'
ANCHORBANK_LOCATION = os.path.join(GTAB_DIR, 'output/google_anchorbanks', ANCHORBANK)

t = gtab.GTAB(dir_path=GTAB_DIR)
t.set_options(pytrends_config={'geo': '',  # Query the whole world. (Alternatively, 2 letter country code)
                               'timeframe': TIMEFRAME})
if not os.path.exists(ANCHORBANK_LOCATION):
    print("Creating Anchorbank...")
    t.create_anchorbank()

t.set_active_gtab(ANCHORBANK)


with open('keywords.txt', 'r') as keywords:
    terror_kws = sorted([s.strip() for s in keywords.readlines()])


def query(keywords, fname=None):
    ret = {}

    for kw in keywords:
        q = t.new_query(kw)
        if isinstance(q, int):  # Not able to calibrate
            assert q == -1, "Query returns unknown code."
            print("NO CALIBRATION")
            continue
        ret[kw] = q

    if fname is not None:
        with open(fname, 'wb') as query_result:
            pickle.dump(ret, query_result)

    return ret


try:
    with open(TERROR_FILE, 'rb') as terror:
        terror = pickle.load(terror)
        print("Loaded google trends dataset.")
except FileNotFoundError:
    print("No terrorism google trends found. Querying now...")
    terror = query(terror_kws, TERROR_FILE)
except EOFError:
    print("Saved trends file seems to be corrupted. New query...")
    terror = query(terror_kws, TERROR_FILE)

terror_df = pd.concat(terror.values(), keys=terror.keys()).reset_index()
terror_df.rename(columns={'level_0': 'article'}, inplace=True)
terror_df['date'] = pd.to_datetime(terror_df['date'])
print(terror_df.sample(frac=1).head())
