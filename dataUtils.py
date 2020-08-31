# Version     : 1.0
# Author      : James Allington-Kay
# Script Name : dataUtils.py

import pandas as pd
from datetime import datetime
import requests

INDICES_URL = 'https://www.theice.com/cds/MarkitIndices.shtml'
SN_URL      = 'https://www.theice.com/cds/MarkitSingleNames.shtml'


def _getSettlementPricesRaw(url):
    '''Raw call to ICE to get the EOD spreads for either idx or sn'''

    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    out = pd.read_html(r.text)
    if out:
        return out[0]
    

def getEODCDSIndexSpreads():
    ''' Pulls the EOD Settlement prices from ICE (Markit Sourced) using 
        publically available data, only for T-1 for Credit Indices (Itraxx Europe Main & Crossover, 
        CDX NA High Yield & IG (Investment Grade)) '''

    data = _getSettlementPricesRaw(INDICES_URL)
    out = {}
    for _, d in data.iterrows():
        out[d.Instrument] = {'conventionalSpread5y': d['EOD Spread'], 'price5y': d['EOD Price'], 'pricingDate' : d['Date']}


def getEODCDSSingleNameSpreads():
    ''' - Pulls the EOD Settlement prices from ICE (Markit Sourced) using publically available data, 
        only for T-1 for Single Name Corporates. 
        - Keyed by instrument 5 key (markitTicker.seniority.ccy.docClause.coupon.maturity). 
        - Price is in percentage terms (100 - EOD Price will get to the uprfront) '''

    data = _getSettlementPricesRaw(SN_URL)
    out = {}
    for _, d in data.iterrows():
        markitTicker, seniority, ccy, tier, coupon, maturity = d['Instrument'].split('.')
        out[d.Instrument] = { 'price5y'      : d['EOD Price'], 
                              'entityName'   : d['Name'], 
                              'pricingDate'  : d['Date'], 
                              'coupon'       : coupon, 
                              'ccy'          : ccy,
                              'docClause'    : tier,
                              'maturity'     : datetime.strptime(maturity, '%Y-%m-%d'),
                              'seniority'    : seniority,
                              'markitTicker' : markitTicker }

    return out

print(getEODCDSSingleNameSpreads())