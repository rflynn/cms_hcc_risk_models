mkdir -p data/cpt_hcpc_2017
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2017-Medicare-CPT-HCPC-List.zip -P data/cpt_hcpc_2017
unzip data/cpt_hcpc_2017/2017-Medicare-CPT-HCPC-List.zip -d data/cpt_hcpc_2017


mkdir -p data/cpt_hcpc_2016
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2016-Medicare-CPT-HCPC-List.zip -P data/cpt_hcpc_2016
unzip data/cpt_hcpc_2016/2016-Medicare-CPT-HCPC-List.zip -d data/cpt_hcpc_2016


mkdir -p data/cpt_hcpc_2015
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2015-Medicare-CPT-HCPCS-Codes.zip -P data/cpt_hcpc_2015
unzip data/cpt_hcpc_2015/2015-Medicare-CPT-HCPCS-Codes.zip -d data/cpt_hcpc_2015


mkdir -p data/cpt_hcpc_2014
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2014-Medicare-CPT-HCPCS-Codes.zip -P data/cpt_hcpc_2014
unzip data/cpt_hcpc_2014/2014-Medicare-CPT-HCPCS-Codes.zip -d data/cpt_hcpc_2014

# get CMS models
#======================================================================

#2017 model
#------------------------------------------
mkdir -p cms_models/2017
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2017-Initial-Model.zip -P cms_models/2017
unzip cms_models/2017/2017-Initial-Model.zip -d cms_models/2017

mkdir -p cms_models/2017/cms_hcc_v2216_79_02
mkdir -p cms_models/2017/rxhcc_r0516_76_01

unzip 'cms_models/2017/CMS-HCC software V2216.79.O2.zip' -d cms_models/2017/cms_hcc_v2216_79_02
unzip 'cms_models/2017/RxHCC software R0516.76.O1.zip' -d cms_models/2017/rxhcc_r0516_76_01

#2016 model
#------------------------------------------
mkdir -p cms_models/2016
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2016-Midyear-Final-Model.zip -P cms_models/2016
unzip cms_models/2016/2016-Midyear-Final-Model.zip -d cms_models/2016

mkdir -p cms_models/2016/cms_hcc_v2116_87_h1
mkdir -p cms_models/2016/cms_hcc_v2216_79_l1
mkdir -p cms_models/2016/esrd_2116_87_h1
mkdir -p cms_models/2016/rxhcc_r0516_76_n2

unzip 'cms_models/2016/CMS-HCC software V2116.87.H1.zip' -d cms_models/2016/cms_hcc_v2116_87_h1
unzip 'cms_models/2016/CMS-HCC software V2216.79.L1.zip' -d cms_models/2016/cms_hcc_v2216_79_l1
unzip 'cms_models/2016/ESRD software E2116.87.H1.zip' -d cms_models/2016/esrd_2116_87_h1
unzip 'cms_models/2016/RxHCC software R0516.76.N2.zip' -d cms_models/2016/rxhcc_r0516_76_n2
