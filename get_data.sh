mkdir -p data/cpt_hcpc_2017
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2017-Medicare-CPT-HCPC-List.zip -P data/cpt_hcpc_2017
#unzip data/cpt_hcpc_2017/2017-Medicare-CPT-HCPC-List.zip -d data/cpt_hcpc_2017


mkdir -p data/cpt_hcpc_2016
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2016-Medicare-CPT-HCPC-List.zip -P data/cpt_hcpc_2016
#unzip data/cpt_hcpc_2016/2016-Medicare-CPT-HCPC-List.zip -d data/cpt_hcpc_2016


mkdir -p data/cpt_hcpc_2015
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2015-Medicare-CPT-HCPCS-Codes.zip -P data/cpt_hcpc_2015


mkdir -p data/cpt_hcpc_2014
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2014-Medicare-CPT-HCPCS-Codes.zip -P data/cpt_hcpc_2014


# get CMS models
mkdir -p cms_models/2017
wget -nc https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/Downloads/2017-Initial-Model.zip -P cms_models/2017
#unzip cms_models/2017/2017-Initial-Model.zip -d cms_models/2017
mkdir -p cms_models/2017/cms_hcc
mkdir -p cms_models/2017/rxhcc
#unzip 'cms_models/2017/CMS-HCC software V2216.79.O2.zip' -d cms_models/2017/cms_hcc
#unzip 'cms_models/2017/RxHCC software R0516.76.O1.zip' -d cms_models/2017/rxhcc
