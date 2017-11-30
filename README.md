# fiver

A utility that answers one question: How many units are available during a response system's busiest 5 minute period?

## Installation

Using [pip](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip):
```
pip install git+https://github.com/garnertb/fiver.git
```

## Getting Started

In order to use fiver, you'll need to have a CSV with three columns:

* unit_id: The unit's id (ie E525)
* dispatched: The timestamp* when the unit was dispatched.
* available: The timestamp* when the unit cleared the incident.


\* Timestamps should be [ISO-8601  compliant](https://en.wikipedia.org/wiki/ISO_8601).

After installation, you can run `fiver -h` from a terminal to learn more about the tool:

```
Usage: fiver [OPTIONS] INPUT START END

  Calculates the 5 minute time frame with the most units out of service.

Options:
  --pool INTEGER      Number of processes to use.
  --units INTEGER     Total number of units available.
  --count INTEGER     Number of results to return.
  --timezone TEXT     Timezone of data.
  --save / --no-save  Save the file as a csv.
  --help              Show this message and exit.
  ```

  Fiver needs three elements in order to run:
     1. The input CSV file.
     2. The start date (YYYY-MM-DD).
     3. The end date (YYYY-MM-DD).


**Note:** The default timezone for fiver is `US/Eastern`.  Make sure to specify the `--timezone` flag with your actual timezone.

Basic execution:
```
fiver rfd-vehicles.csv 2017-01-01 2017-1-02

# Results
date_time_bin  counts                           units
1  2017-01-01T20:45:00-05:00       8  E5,E16,E23,T22,BC1,BC2,E21,E11
2  2017-01-01T00:15:00-05:00       6             E14,E23,E10,BC3,E16
3  2017-01-01T14:10:00-05:00       5               E5,E15,E11,E22,E6
4  2017-01-01T02:20:00-05:00       5              E21,E1,E11,E16,E18
5  2017-01-01T00:30:00-05:00       5                 E20,E14,E23,E16
```

Here you can see that at 2017-01-01T20:45:00-05:00 8 units were out of service within a 5 minute timeframe.

If you specify the `--units` parameter, the tool will tell you what percentage of units are being utilized:

```
fiver rfd-vehicles.csv 2017-01-01 2017-1-02 --units 8

date_time_bin  counts                           units  \
1  2017-01-01T20:45:00-05:00       8  E5,E16,E23,T22,BC1,BC2,E21,E11   
2  2017-01-01T00:15:00-05:00       6             E14,E23,E10,BC3,E16   
3  2017-01-01T14:10:00-05:00       5               E5,E15,E11,E22,E6   
4  2017-01-01T02:20:00-05:00       5              E21,E1,E11,E16,E18   
5  2017-01-01T00:30:00-05:00       5                 E20,E14,E23,E16   

units_available  utilization  
                0        100.0  
                2         75.0  
                3         62.5  
                3         62.5  
                3         62.5
```
