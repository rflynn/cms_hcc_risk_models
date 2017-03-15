"""
Handle the "formats" file that has all the data in the HCC model except
the regression coefficients.
"""

import pandas


class HccFormats:

    def __init__(self, fname):
        """Read CSV version of formats catalog file"""
        self.fname = fname
        self.df = pandas.read_csv(fname)
        self.parse_tables()

    def parse_tables(self):
        """Split the single DataFrame into tables (e.g. AGEL, AGEU, ...)"""
        self.tables = {}
        for fmtname in self.df['FMTNAME'].unique():
            tbl = self.df[self.df['FMTNAME'] == fmtname]
            tbl = tbl.set_index('START')
            self.tables[fmtname] = tbl.copy()

    def sedit_check_age(self, diag, age, diag_type):
        """Check MCE age restrictions on diagnosis code"""

        valid = True

        if diag_type == 0:
            df = self.tables['I0AGEY16MCE']
        elif diag_type == 9:
            df = self.tables['I9AGEY15MCE']
        else:
            raise ValueError('diag_type must be in [0,9]')

        if diag in df.index:
            _tage = df.loc[diag]['LABEL']
            age_lo = int(self.tables['AGEL'].loc[_tage]['LABEL'])
            age_hi = int(self.tables['AGEU'].loc[_tage]['LABEL'])
            if age < age_lo or age > age_hi:
                valid = False

        return valid

    def sedit_check_sex(self, diag, sex, diag_type):
        """Check MCE sex restrictions on diagnosis code"""

        valid = True

        if diag_type == 0:
            df = self.tables['I0SEXY16MCE']
        elif diag_type == 9:
            df = self.tables['I9SEXY15MCE']
        else:
            raise ValueError('diag_type must be in [0,9]')

        if diag in df.index:
            _tsex = df.loc[diag]['LABEL']
            if int(_tsex) != sex:
                valid = False

        return valid

    def cc_pri_assignment(self, diag, diag_type):
        cc = -1
        if diag_type == 0:
            df = self.tables['I0V22Y16RC']
        elif diag_type == 9:
            df = self.tables['I9V22Y15RC']
        else:
            raise ValueError('diag_type must be in [0,9]')
        if diag in df.index:
            cc = int(df.loc[diag]['LABEL'])
        return cc

    def cc_dup_assignment(self, diag, diag_type):
        cc = -1
        if diag_type == 0:
            df = self.tables['I0DUPV22Y16RC']
        elif diag_type == 9:
            df = self.tables['I9DUPV22Y15RC']
        else:
            raise ValueError('diag_type must be in [0,9]')
        if diag in df.index:
            cc = int(df.loc[diag]['LABEL'])
        return cc

    def cc_sec_assignment(self, diag, diag_type):
        cc = -1
        if diag_type == 0:
            df = self.tables['I0SECV22Y16RC']
        else:
            raise ValueError('diag_type must be in [0]')
        if diag in df.index:
            cc = int(df.loc[diag]['LABEL'])
        return cc


if __name__ == '__main__':

    fname = 'cms_models/2017/cms_hcc_v2216_79_02/F221690P.csv'
    hcc_formats = HccFormats(fname)

    # a few age tests
    diag = 'C9332'
    diag_type = 0
    age = 65
    assert(hcc_formats.sedit_check_age(diag, age, diag_type) is False)
    age = 3
    assert(hcc_formats.sedit_check_age(diag, age, diag_type) is True)

    # a few sex tests
    diag = 'C50321'
    diag_type = 0
    sex = 2
    assert(hcc_formats.sedit_check_sex(diag, sex, diag_type) is False)
    sex = 1
    assert(hcc_formats.sedit_check_sex(diag, sex, diag_type) is True)
