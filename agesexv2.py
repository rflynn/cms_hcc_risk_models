"""
 %MACRO AGESEXV2(AGEF=, SEX=, OREC=);
 %**********************************************************************
 ***********************************************************************
  1  MACRO NAME:     AGESEXV2
  2  PURPOSE:        create demographic variables used in regressions.
  3  PARAMETERS:
                     AGEF     - age variable (integer)
                     SEX      - sex variable (character)
                     OREC     - original reason for entitlement
                                variable from Denominator (character)
  4  CREATED VARIABLES:
                     ORIGDS  - originally disabled dummy variable
                     DISABL  - disabled dummy variable
                     24 dummy agesex variables for all models except
                     "new enrollee":
                     F0_34  F35_44 F45_54 F55_59 F60_64 F65_69
                     F70_74 F75_79 F80_84 F85_89 F90_94 F95_GT
                     M0_34  M35_44 M45_54 M55_59 M60_64 M65_69
                     M70_74 M75_79 M80_84 M85_89 M90_94 M95_GT
                     32 dummy agesex variables for "new enrollee" model:
                     NEF0_34  NEF35_44 NEF45_54 NEF55_59 NEF60_64
                     NEF65    NEF66    NEF67    NEF68    NEF69
                     NEF70_74 NEF75_79 NEF80_84 NEF85_89 NEF90_94
                     NEF95_GT
                     NEM0_34  NEM35_44 NEM45_54 NEM55_59 NEM60_64
                     NEM65    NEM66    NEM67    NEM68    NEM69
                     NEM70_74 NEM75_79 NEM80_84 NEM85_89 NEM90_94
                     NEM95_GT
 ***********************************************************************;
"""

import re
import regression_variables as rv

MAX_AGE = 1000

# gratuitous use of regular expressions
PATTERN = re.compile(
    """
    (NE)?                    # optional 'NE' prefix
    (?P<sex>M|F)             # sex
    (?P<age_lo>\d{1,2})      # lower age limit
    (_                       # underscore
    (?P<age_hi>\d{1,2}|GT)   # upper age limit
    )?
    """, re.VERBOSE)


def parse_agesex_var(x):
    """Take a string of the form NEF65 or NEF95_GT and return sex and
    age range.
    """
    m = re.match(PATTERN, x)
    sex = 1 if m.group('sex') == 'M' else 2
    age_lo = m.group('age_lo')
    age_hi = m.group('age_hi')
    if age_hi == 'GT':
        age_hi = MAX_AGE
    if age_hi is None:
        age_hi = age_lo
    return sex, int(age_lo), int(age_hi)


def create_demographic_regression_variables(age, sex, orec):

    print('age={}, sex={}, orec={}'.format(age, sex, orec))

    # %**********************************************************************
    # *  disabled, originally disabled variables
    # ***********************************************************************;

    # disabled ?
    disabl = int(age < 65 and orec != 0)

    # originally disabled
    origds = int(orec == 1 and disabl)

    print('disabl={}, origds={}'.format(disabl, origds))

    # %**********************************************************************
    # * variables for all models exept "new enrollee"
    # ***********************************************************************;
    cell = {key: 0 for key in rv.AGESEXV}
    for key in rv.AGESEXV:
        key_sex, key_age_lo, key_age_hi = parse_agesex_var(key)
        if sex == key_sex and key_age_lo <= age <= key_age_hi:
            cell[key] = 1
    print('cell={}'.format(cell))

    # %**********************************************************************
    # * age/sex vars for "new enrollee"  model
    # ***********************************************************************;
    necell = {key: 0 for key in rv.NE_AGESEXV}
    for key in rv.NE_AGESEXV:
        key_sex, key_age_lo, key_age_hi = parse_agesex_var(key)
        if sex == key_sex and key_age_lo <= age <= key_age_hi:
            necell[key] = 1

    print('necell={}'.format(necell))

    return disabl, origds, cell, necell
