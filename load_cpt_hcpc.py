import pandas
import codecs


FNAMES = {
    2017: 'data/cpt_hcpc_2017/2017 Medicare CPT HCPC List.csv',
    2016: 'data/cpt_hcpc_2016/2016 Medicare CPT HCPC List.csv',
}


def read_csv(year):
    fname = FNAMES[year]
    with codecs.open(fname, 'r', encoding='utf-8', errors='ignore') as fdata:
        df = pandas.read_csv(fdata, header=2)
        df = df.dropna()
    return df
