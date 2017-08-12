# MortgageCalculator
Some simple code to run mortgage calculations

## Running the code.
(Hi Phil!)
Hopefully it's pretty self explanatory.

- Initialise the model with *current* savings and house price.

- Run the pre-purchase method to account for house price growth and savings
  growth before the purchase. Then call the loan start method.

- So far that'll get you things like repayments, purchase price, etc. You can
  then run the model loan method to model a repayment schedule for a fixed
  period (the repayments are assumed to be monthly and passed in as a list). You
  can optionally continue on the calculation with a new repayment schedule.

My testing of this shows that it gets it mostly right, stamp duty is for ACT,
LMI is cribbed from some website.
