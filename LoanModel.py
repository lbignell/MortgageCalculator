import numpy as np
import matplotlib.pyplot as plt

class LoanModel():
    def __init__(self, totsavings, houseprice, income, interest,
                 dutyapplied=True):
        '''
        instanciate a loan model with parameters.
        All incomes/rates are annual.
        DON'T include LMI or duties.
        '''
        self.savings = totsavings
        self.houseprice = houseprice
        self.income = income
        self.interest = interest
        if dutyapplied:
            self.calc_stamp_duty()
        else:
            self.stamp_duty = 0
        self.principalnow = None
        self.history_payments = None
        self.history_principal = None
        self.payments_peryr = 12
        return

    def pre_purchase(self, delay_y, savingrate_y, pricegrowthrate):
        '''
        Adjust savings, etc. for delaying a purchase by some period.
        '''
        self.savings += savingrate_y*delay_y
        self.houseprice += pricegrowthrate*self.houseprice*delay_y
        return

    def post_purchase(self):
        self.postMortgageIncome = self.income + self.repayments
        self.totalinterest30Y = self.repayments*30 + self.borrowed #Over whole loan
        return

    def model_loan(self, payschedule, carryon=False):
        '''
        This models the loan, either carrying on from principalnow or starting
        fresh from borrowed. payschedule is a list of monthly payments, as a
        list.
        '''
        if carryon:
            if self.principalnow is None:
                print("ERROR: Can't carry on")
                raise ValueError
            self.history_payments += payschedule
        else:
            self.principalnow = self.borrowed
            self.history_principal = []
            self.history_payments = payschedule

        for thepayment in payschedule:
            self.principalnow -= thepayment + np.ipmt(self.interest, 1, self.loanterm,
                                                      self.principalnow)/self.payments_peryr
            self.history_principal += [self.principalnow]

        return

    def calc_stamp_duty(self):
        '''
        Using this site:
        https://www.revenue.act.gov.au/duties-and-taxes/duties/non-commercial-transfer-duty
        '''
        rates = {200000: 0.014, 300000: 0.024, 500000: 0.038,
                 750000: 0.0478, 1000000: 0.063}

        if self.houseprice > 1454999:
            self.stamp_duty = 0.0491*self.houseprice
            return

        self.stamp_duty = 0
        prev_thresh = 0
        for thresh, item in rates.items():
            if self.houseprice > thresh:
                self.stamp_duty += (thresh - prev_thresh)*item
                prev_thresh = thresh
            else:
                self.stamp_duty += (self.houseprice - prev_thresh)*item
                break

        return

    def calc_LMI(self):
        '''
        Calculate LMI, using yourmortgage.com.au calculator at 750000 property
        value to calibrate. The points seem to scale linearly with the house price.
        '''
        calibLVR = np.array([0.95, 0.925, 0.9, 0.875, 0.85, 0.825, 0.8])
        calibLMI = np.array([35198, 29693, 16740, 11681, 9116, 7178, 0])
        calibprice = 750000
        self.LMI = (self.houseprice/calibprice)*np.interp(self.LVR, 1-calibLVR,
                                                          calibLMI)
        return

    def loan_start(self):
        '''
        Initiate the loan: 
        
        - all savings go to deposit
        
        - stamp duty is calculated at a fixed rate and comes out of the deposit
        
        - LMI is applied, if applicable.
        '''
        self.deposit = self.savings - self.stamp_duty
        self.LVR = self.deposit/self.houseprice
        if self.LVR < 0.2:
            #Need LMI
            self.calc_LMI()
        else:
            self.LMI = 0

        
        self.loanterm = 30 #years
        self.borrowed = self.houseprice - self.deposit + self.LMI
        self.repayments = np.pmt(self.interest,
                                 self.loanterm, 
                                 self.borrowed)
        return


