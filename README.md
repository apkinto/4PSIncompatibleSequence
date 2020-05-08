# 4PSIncompatibleSequence
Flag an operation as incompatible if it follows a specific item

- Requires some cleaning up (add logging?) and other potential exception handling to make it more robust
- Since this is being run from the applicaiton it is looking for the config file in PS bin...need to change to look for it in the script location.
- Current attribute and attribute value to set are hard coded, consider parameterizing
- May want to change definition of incompatible sequences from the xml config to a spreadsheet, csv or another approach
