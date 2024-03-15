# Miniproject2_brights
Repo for project2

This should be a working model now.

The 'data' folder includes the data the ETL and ML scripts are designed to run on. The files have been preprocessed before this, so it doesn't run on what you get from FMI directly.

etl.py does some ETL for the data per venue.

ml1.py creates and trains the ML models based on four venues.

ml2.py tests the models against another venue.

ml3.py attempts to predict the snow depth for the next 20 years. Doesn't work, but looks neat I guess.

sql.py creates tables in a postgres and populates them with data per venue. Requires a running DB.
