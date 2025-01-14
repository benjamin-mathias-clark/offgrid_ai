A Python implementation of the LCOE workbook published by offgridai.us.

## Files
- offgrid_ai.py: The core implementation of the financials and calculation of the LCOE.
- offgrid_ai.proto - Protocol buffer representation of the data structures involved.
- offgrid_ai_pb2.py - For convenience, the compiled version of the proto file above.
- offgrid_ai_data.binarypb - This has all the data from the data sheet in the [workbook](https://www.offgridai.us/offgrid-ai-lcoe-calculator.xlsm) in the protocol buffer format. Specifically, for a range of different solar and battery sizes, sytems locations and gas generator/turbines sizes, this has 20 years of annual data on solar production, battery throughput and natural gas production.
- test_offgrid_ai.py: Runs a set of basic LCOE calculations as a demonstration example. Also used for comparing results against those in the workbook.
- offgrid_ai_parameter_sensitivity.py: A more thorough example of using this to test out a wider set of scenarios.

## Example Results

The cost optimal system changes based on the prices of different inputs. For instance, we can look
at how the optimal system responds to price decreases in solar panels & batteries. The resultant
data is available [here](https://docs.google.com/spreadsheets/d/1UkHo5jvbne0NTeN4YN14w7xSIiwNQm8X2MwY919CE3M/view)
and we can see how the LCOE, lifetime renewable percentage, solar size and battery size all change
in response to these input prices. Additionally, we can see how that response is different under a
30% and 40% ITC.

We can also generate Pareto frontiers of the tradeoff between LCOE & lifetime renewable percentage for
different scenarios. [Here](https://docs.google.com/spreadsheets/d/1DhBXOtFV8JG6RKbbflTKTjYoUsvOSao7G8KFcswaPzU/view)
are the Pareto frontiers for both the standard 30% ITC and the 40% energy community ITC.
