import gtab
import pandas as pd
import pickle
import os


class TrendsQueryer:

    PARENT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    GTAB_DIR = os.path.join(PARENT_DIRECTORY, 'gtab/')
    GOOGLE_DATA_LOCATION = os.path.join(PARENT_DIRECTORY, 'data/google-trends/')
    QUERY_TERM_LOCATION = os.path.join(PARENT_DIRECTORY, 'data/query-terms')

    def __init__(self, timeframe, geo_code=''):
        self.timeframe = timeframe
        geo_code = geo_code.upper()
        self.anchorbank = 'google_anchorbank_geo=' + geo_code + '_timeframe=' + timeframe + '.tsv'
        self.t = gtab.GTAB(self.GTAB_DIR)
        self.t.set_options(pytrends_config={'geo': geo_code,
                                            'timeframe': timeframe})
        if not os.path.exists(os.path.join(self.GTAB_DIR, 'output/google_anchorbanks/', self.anchorbank)):
            print("Creating Anchorbank...")
            self.t.create_anchorbank()
        self.t.set_active_gtab(self.anchorbank)

    def query_keywords(self, keywords, fname=None):
        query_dict = {}

        for kw in keywords:
            q = self.t.new_query(kw)
            if isinstance(q, int):  # Not able to calibrate
                assert q == -1, "Query returns unknown code."
                print("NO CALIBRATION POSSIBLE FOR: {}".format(kw))
                continue
            query_dict[kw] = q

        df = pd.concat(query_dict.values(), keys=query_dict.keys()).reset_index().rename(columns={'level_0': 'article'})
        if len(fname.split('_')) == 2:
            df['lanuage'] = fname.split('_')[-1]
        else:
            df['lanugage'] = None

        if fname is not None:
            fpath = os.path.join(self.GOOGLE_DATA_LOCATION, fname)
            df.to_csv(fpath, index=False)

        return df

    def load_or_query(self, trends):
        if not trends.endswith('.csv'):
            trends_file = trends + '.csv'
        else:
            trends_file = trends
        if os.path.exists(trends_file):
            file_loc = trends_file
        else:  # Usually we declare a filename, the file itself is stored in the default directory.
            file_loc = os.path.join(self.GOOGLE_DATA_LOCATION, trends_file)
        try:
            query = pd.read_csv(file_loc)
            print("Loaded", trends_file)
        except FileNotFoundError:
            print("No file {} found. Querying now...".format(file_loc))
            query_terms = os.path.join(self.QUERY_TERM_LOCATION, trends_file.replace('.csv', '.txt'))
            if not os.path.exists(query_terms):
                print("Querying failed. Keywords to use unknown.")
                return
            with open(query_terms, 'r') as qt:
                keywords = sorted([s.strip().replace('_', ' ') for s in qt.readlines()])
            query = self.query_keywords(keywords, fname=trends_file)

        return query
