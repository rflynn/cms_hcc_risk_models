"""
 * set the following parameters:
 *      INP      - SAS input person dataset
 *      IND      - SAS input diagnosis dataset
 *      OUTDATA  - SAS output dataset
 *      IDVAR    - name of person id variable (HICNO for medicare data)
 *      KEEPVAR  - variables to keep in the output dataset
 *      SEDITS   - a switch that controls whether to perform MCE edits
 *                 on ICD9 and ICD10: 1-YES, 0-NO
 *      DATE_ASOF- reference date to calculate age. Set to February 1
 *                 of the payment year for consistency with CMS

 %V2216O2M(INP      =IN1.PERSON,
           IND      =IN2.DIAG,
           OUTDATA  =OUT.PERSON,
           IDVAR    =HICNO,
           KEEPVAR  =HICNO &INPUTVARS &SCOREVARS &DEMVARS
                     &HCCV22_list79 &CCV22_list79,
           SEDITS   =1,
           DATE_ASOF="1FEB2016"D);


"""

import datetime
import v221602p



idvar = 'HICNO'
keepvar = [idvar] + v221602p.input_vars + v221602p.scorevars + \
          v221602p.dem_vars + v221602p.hccv22_list79 + v221602p.ccv22_list79
sedits = 1
date_asof = datetime.date(2016, 2, 1)
