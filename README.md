# Python Credit Derivatives
Utils for Credit Derivatives in Python

## dataUtils.py Usage
### _getSettlementPricesRaw
Raw call to ICE to get the EOD spreads for either idx or sn.
### getEODCDSIndexSpreads
Pulls the EOD Settlement prices from ICE (Markit Sourced) using publically available data, only for T-1 for Credit Indices (Itraxx Europe Main & Crossover, CDX NA High Yield & IG (Investment Grade))
### getEODCDSSingleNameSpreads
Pulls the EOD Settlement prices from ICE (Markit Sourced) using publically available data, only for T-1 for Single Name Corporates. Keyed by instrument 5 key (markitTicker.seniority.ccy.docClause.coupon.maturity). Price is in percentage terms (100 - EOD Price will get to the uprfront)