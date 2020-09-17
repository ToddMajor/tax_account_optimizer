'''
The point of this program is to determine if it is better to use a traditional (pre-tax 401k)
or use a Roth 401k. Todd postulates that the only important thing is the tax rate now versus 
the tax rate later.
'''


class Base():
    '''
    This will be the base class that we will use to make all the equations. We will make sub classes
    that inherit the equations, but will have their own variables for tax rates, etc.
    '''

    def __init__(self):
        self.income = 100000
        self.health_payment = 0
        self.corr_income = self.income - self.health_payment
        self.social_security_rate = 0.062
        self.medicare_rate = 0.0145
        self.required_takehome = 50000
        self.required_takehome_retirement = 50000

    def social_security_medicare_payment(self):
        return self.corr_income*(self.social_security_rate+self.medicare_rate)

    def adjusted_gross_income(self):
        return self.corr_income - self.trad_401k - self.standard_deduction

    def federal_tax_payment(self):
        taxes = 0
        for a in self.federal_tax_rates:
            if self.adjusted_gross_income() > a[2]:
                taxes += ((a[2]-a[1])*a[0])
            elif self.adjusted_gross_income() <= a[2]:
                taxes += ((self.adjusted_gross_income() - a[1])*a[0])
                return taxes 

    def state_tax_payment(self):
        return self.illinois_tax_rate*self.adjusted_gross_income()
    
    def calculate_yearly_takehome(self):
        return self.corr_income - self.social_security_medicare_payment() - self.trad_401k - self.federal_tax_payment() - self.state_tax_payment() - self.roth_401k

    def retirement_401k_compounding(self, account_type, years, interest_rate):

        '''replace with account componding so I can use trad, roth, and taxable options'''

        if account_type == "t":
            account = self.trad_401k
        elif account_type == "r":
            account = self.roth_401k
        elif account_type == "taxable":
            account = self.excess_income()
        retirement_account = account #starting value at year 0
        for year in range(1, years+1):
            retirement_account = retirement_account*(1+interest_rate) + account
            #print(f"You would have {account} after {year} years.")
        return retirement_account   

    def federal_tax_payment(self):
        taxes = 0
        for a in self.federal_tax_rates:
            if self.adjusted_gross_income() > a[2]:
                taxes += ((a[2]-a[1])*a[0])
            elif self.adjusted_gross_income() <= a[2]:
                taxes += ((self.adjusted_gross_income() - a[1])*a[0])
                return taxes 

    def state_tax_payment(self):
        return self.illinois_tax_rate*self.adjusted_gross_income()
    
    def calculate_yearly_takehome(self):
        return self.corr_income - self.social_security_medicare_payment() - self.trad_401k - self.federal_tax_payment() - self.state_tax_payment() - self.roth_401k

    def excess_income(self):
        return self.calculate_yearly_takehome() - self.required_takehome

class Single(Base):

    '''
    10%-- $0 to $9875
    12%-- $9876 to $40125
    22%-- $40126 to $85525
    24%-- $85526 to $163000
    32%-- $163301 to $207350
    '''

    def __init__(self):
        super().__init__()
        self.roth_401k = 19000
        self.federal_tax_rates = [  (0.1, 0, 9875),
                                    (0.12, 9876, 40125),
                                    (0.22, 40126, 85525),
                                    (0.24, 85526, 163000),
                                    (0.32, 163301, 207350)
                                    ]
        self.long_term_taxable_tax_rates = [    (0, 0, 40000),
                                                (0.15, 40001, 441450),
                                                (0.20, 441451, 1000000000)]
        self.illinois_tax_rate = 0.0495
        self.trad_401k = 0
        self.standard_deduction = 12000



class Married_With_Children(Base):

    '''
    10%-- $0 to $19750  
    12%-- $19751 to $80250
    22%-- $80251 to $171050
    24%-- $171051 to $326600
    32% --$326601 to $414700

    '''

    def __init__(self):
        super().__init_()
        self.roth_401k = 0
        self.federal_tax_rates = [  (0.1, 0, 19750),
                                    (0.12, 19751, 80250),
                                    (0.22, 80251, 171050),
                                    (0.24, 171051, 326600),
                                    (0.32, 326601, 4147000)
                                    ]
        self.long_term_taxable_tax_rates = []
        self.illinois_tax_rate = 0.0495
        self.trad_401k = 0
        self.standard_deduction = 24000

def App():
    app = Single()
    value = app.calculate_yearly_takehome()
    #trad_401k = app.retirement_401k_compounding("t", 30, 0.07)
    roth_401k = app.retirement_401k_compounding("r", 30, 0.07)
    #print(f"Yearly takehome is: {value}")
    print(f"Excess income for taxable account is {app.excess_income()}")
    #print(f"Traditional 401k has a value of {trad_401k} after 30 years.")
    print(f"Roth 401k has a value of {roth_401k} after 30 years.")
    print(f"Taxable Account has a value of {app.retirement_401k_compounding('taxable', 30, 0.07)} after 30 years.")

    #print(f"Roth 401k has a value of {roth_401k} after 30 years.")


if __name__ == "__main__":
    App()

