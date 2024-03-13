# Miniproject2_brights
Repo for project2

The CSV's should be in such an order that by running the __init__ file, you'll get a new folder "Finished CSVs" in your project root folder.

These files are the per venue files that should be ready for ML. Need to check datatypes etc.

The CSV's themselves have been preprocessed a bit. The short story is:
- The small batches were concatenated
- The venues where the daily means for cloud coverage weren't working as intended were redownloaded with momentary observations from which the daily means were calculated via script after concatenating them
- - This fixed the issue of a single missing reading causing the daily mean to be missing as well
- Solar radiation was taken from several points and is one file that is used by every venue
- - Geographical location varies but the thought is that at least annual solar cycles will be considered in a grander sense

The preprocessed CSV's are basically the avg temp & snowdepth per venue, the cloud coverage daily mean per venue and the solar radiation, and from these are generated the finished CSV's per venue

work.py has the functions

salpausselkädataconcat.py is for posterity to see what was done with the salpausselkä data initially, this can be ignored

calculatedailymeansforcloudcoverage.py is the script used to calculate the daily means from momentary observation data regarding cloud coverage
It has to be manually set to find the files, although it could be automated easily provided the input files are standardized
