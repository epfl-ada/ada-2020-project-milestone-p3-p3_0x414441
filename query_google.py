## !pip install gtab
import gtab
import pandas as pd
import pickle
TERROR_FILE = 'google_terrorism.obj'
TIMEFRAME = '2011-01-01 2015-12-31'

t = gtab.GTAB(dir_path='./gtab')
t.set_options(pytrends_config={'geo': '',  # Query the whole world. (Alternatively, 2 letter country code)
                               'timeframe': TIMEFRAME})
t.create_anchorbank()
t.set_active_gtab('google_anchorbank_geo=_timeframe=' + TIMEFRAME + '.tsv')

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
            pickle.dump(result, query_result)

    return ret


try:
    with open(TERROR_FILE, 'rb') as terror:
        terror = pickle.load(terror)
except FileNotFoundError:
    print("No terrorism google trends found. Querying now...")
    terror = query(terror_kws, TERROR_FILE)

terror_df = pd.concat(terror.values(), key=terror.keys())
print(terror_df.head())
