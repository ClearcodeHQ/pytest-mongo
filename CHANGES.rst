CHANGELOG
=========

2.0.0
-------

- [feature] Allow for mongo client to be configured with time zone awarness
- [feature] Drop support for python 2.7. From now on, only support python 3.6 and up

1.2.1
-------

- fix pypi description

1.2.0
-------

- [enhancement] require at least pymongo 3.6

1.1.2
-------

- [enhancement] removed path.py depdendency

1.1.1
-------

- [enhancements] set executor timeout to 60. By default mirakuru waits indefinitely, which might cause test hangs

1.1.0
-------

- [feature] - migrate usage of getfuncargvalue to getfixturevalue. require at least pytest 3.0.0

1.0.0
-------

- [feature] defaults logs dir to $TMPDIR by default
- [feature] run on random port by default (easier xdist integration)
- [feature] add command line and ini option for: executable, host, port, params and logsdir
