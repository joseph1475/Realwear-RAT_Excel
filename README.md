#Realwear UI Automation

Automation framework to execute UI test on HMT

To Execute all tabs in Excel:
```
py.test --capture=tee-sys
```
To Execute single tab in Excel:
```
py.test --capture=tee-sys -k <tab_name>   
```

Excel path has to be entered when prompted