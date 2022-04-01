loggingex
==========

Extension of python library logging.
For non-resident python batch logging
The standard RotatingFileHandler or TimedRotatingFileHandler specifications
I didn't like it so I created it.
The content is only MyTimedRotatingFileHandler of handlers.py.

- Unlike TimedRotatingFileHandler, it also supports non-resident processes.
     - For example, if you set when='D', the date will be entered in the log file name and the log will switch every day.
         - Y, M, D, H, MI can be specified as the division unit.
- The log file name retains the specified extension.
- There is no function to delete old log files.

Usage
-----

```ini
[handler_file]
class=loggingex.handlers.MyTimedRotatingFileHandler
args=('myapp.log', 'd', 'utf-8')
```

Demo
-----

```
py -m loggingex
```
