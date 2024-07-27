#Author: Alec Barry
#Cohort: Software Development 12
#Title: One Stop Insurance Company Claim Processor
#Due July 26th, 2024

#Import libraries

import datetime
import FormatValues as FV
import sys
import time


#Define lists

Provinces = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"]
PayPlans = ["Full", "Monthly", "Downpay"]


#Define Constants by constructing a list

f = open("Const.dat", "r")

for Constant in f:
    ConstantList = Constant.split(",")

    POLICY_NUM = int(ConstantList[0].strip())
    BASIC_PREMIUM = float(ConstantList[1].strip())
    ADD_CAR_DISCOUNT = float(ConstantList[2].strip())
    EXTRA_LIAB_COST = float(ConstantList[3].strip())
    GLASS_COST = float(ConstantList[4].strip())
    LOANER_COVERAGE = float(ConstantList[5].strip())
    HST_RATE = float(ConstantList[6].strip())
    MONTHLY_PROC = float(ConstantList[7].strip())

f.close()


#Define functions

def LoadingBar(iteration, total, prefix='',suffix='',length=25,fill='█'):

    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

def LongDate(DateValue):
    
    DateValueStr = DateValue.strftime("%Y, %B, %d")

    return DateValueStr

def FormatPhone(phone_number):
   return f"({phone_number[-10:-7]})-{phone_number[-7:-4]}-{phone_number[-4:]}"


#Main Loop

while True:

    CustFirstName = input("Enter the customer's first name: ").title()
    CustSurname = input("Enter the customer's surname: ").title()
    CustAddress = input("Enter the customer's address: ")
    CustomerCity = input("Enter the customer's city: ").title()

    while True:
        CustomerProvince = input("Enter the customer's province/territory (XX): ").strip().upper()
        if CustomerProvince in Provinces:
            break
        else:
            print("Error: You've entered an invalid province. Please enter the correct 2-character abbreviation (XX).")

    CustomerPostal = input("Please enter the customer's postal code(X#X#X#): ")

    while True:
        CustomerPhone = input("Please enter the customer's phone number(###-###-####): ")
        if len(CustomerPhone) != 10:
            print("Error: Phone number must be 10 characters.")
        else:
            break

    while True:
        NumCarsIns = input("Please enter the number of cars being insured: ")
        NumCarsIns = int(NumCarsIns)
        if NumCarsIns > 0:
            break
        else:
            print("Error: Number of cars insured must be a positive integer.")


    while True:    
        ExtraLiab = input("Is extra liability included (Y/N)?: ").upper()
        if ExtraLiab == "Y" or ExtraLiab == "N":
            break
        else: 
            print("Error: You've entered an invalid option. Please enter Y(for yes), or N(for no).")

    while True: 
        OptionalGlass = input("Is optional glass coverage included (Y/N)?: ").upper()
        if OptionalGlass == "Y" or OptionalGlass == "N":
            break
        else: 
            print("Error: You've entered an invalid option. Please enter Y(for yes), or N(for no).")

    while True:
        LoanerCar = input("Is an optional loaner car included (Y/N)?: ").upper()
        if LoanerCar == "Y" or LoanerCar == "N":
            break
        else: 
            print("Error: You've entered an invalid option. Please enter Y(for yes), or N(for no).")

    while True:
        print()
        print("Payment plan options:")
        print()
        print("Full: Customer pays in-full")
        print("Monthly: Customer pays in monthly installments")
        print("Downpay: Customer has provided a down payment for their installments")
        print()
        CustPayPlan = input("Enter the customer's choice of pay plan (Full, Monthly, Downpay): ").strip().title()
        if CustPayPlan == "Downpay":
            DownPaymentAmt = float(input("Enter the amount of the down payment:").strip())
        if CustPayPlan in PayPlans:
            break
        else:
            print("Error: You've entered an invalid payment plan. Please refer to the provided list for the specific 3 options.")


    ClaimNumbers = []
    ClaimDates = []
    ClaimAmounts = []

    while True:
        ClaimNumber = input("Enter the claim number: ")
        while True:
            ClaimDate = input("Enter the date of the claim (YYYY-MM-DD): ")
            try:
                ClaimDate = datetime.datetime.strptime(ClaimDate, "%Y-%m-%d")
                break
            except:
                print("Error: Date must be in the format YYYY-MM-DD. Please try again.")

        
        while True:
            ClaimAmount = float(input("Enter the claim amount: "))
            if ClaimAmount >= 0:
                break
            else:
                print("Error: Claim amount must be zero or a positive amount.")

        ClaimNumbers.append(ClaimNumber)
        ClaimDates.append(ClaimDate)
        ClaimAmounts.append(ClaimAmount)

        AdditionalClaims = input("Do you wish to enter another claim (Y/N): ").strip().upper()
        if AdditionalClaims != "Y":
            break

    Iterations = 30 
    Message = "Saving your claim data. Please stand by..."
    print(Message)
    for i in range(Iterations + 1):
        time.sleep(0.1)  
        LoadingBar(i, Iterations, suffix='Complete', length=50)
    

    #Perform Calculations

    CurrentTime = datetime.datetime.now()
    CurrentTimeDSP = CurrentTime.strftime("%Y-%m-%d")

    TotalPrevClaimAmt = sum(ClaimAmounts)

    BasePremium = BASIC_PREMIUM + (NumCarsIns - 1) * (BASIC_PREMIUM * (1 - ADD_CAR_DISCOUNT/100))
    ExtraCost = 0
    if ExtraLiab == "Y":
        ExtraCost += EXTRA_LIAB_COST * NumCarsIns
    if OptionalGlass == "Y":
        ExtraCost += GLASS_COST * NumCarsIns
    if LoanerCar == "Y":
        ExtraCost += LOANER_COVERAGE * NumCarsIns

    TotalPremium = BasePremium + ExtraCost
    HST = TotalPremium * HST_RATE 
    TotalCost = TotalPremium + HST

    if CustPayPlan == "Monthly":
        MonthlyPayment = (TotalCost + MONTHLY_PROC) / 8
    elif CustPayPlan == "Downpay":
        MonthlyPayment = (TotalCost - DownPaymentAmt + MONTHLY_PROC) / 8
    
    if CurrentTime.month == 12:
        FirstPaymentDate = CurrentTime.replace(year=CurrentTime.year + 1, month=1, day=1)
    else:
        FirstPaymentDate = CurrentTime.replace(month=CurrentTime.month + 1, day=1)

    

    #Display Results

    print()
    print("                    ----------------------")
    print("                    | One Stop Insurance |")
    print("                    ----------------------")
    print("==================================================================")
    print(f"Policy#: {int(POLICY_NUM)}                                   Date: {CurrentTimeDSP}") 
    print(f"Customer: {CustFirstName} {CustSurname}")
    print(f"Address: {CustAddress}, {CustomerCity}, {CustomerProvince}")
    print()
    print("==================================================================")
    print(f"Postal Code: {CustomerPostal:<7}           |            Number of cars: {NumCarsIns:>6d}")
    print(f"Phone: {FormatPhone(CustomerPhone):<13}          |            Extra Liability: {ExtraLiab:>5}")
    print(f"                               |            Optional Glass: {OptionalGlass:>6}")
    print(f"                               |            Loaner Car: {LoanerCar:>10}")
    print("==================================================================")
    print(f"Payment Plan: {'Down Payment' if CustPayPlan == 'Downpay' else CustPayPlan}")  #This line utilizes an if-statement within the print statement to assign a different value on a specific case
    print("------------")
    print()
    
    if CustPayPlan == "Downpay":
        print(f"Down payment amount:      {FV.FDollar2(DownPaymentAmt)}")
    print(f"Premium Cost:           {FV.FDollar2(BasePremium)}")
    print(f"Extra Cost:               {FV.FDollar2(ExtraCost)}")
    print("---------------------------------")
    print(f"Total Premium:          {FV.FDollar2(TotalPremium)}")
    print(f"HST:                      {FV.FDollar2(HST)}")
    print("---------------------------------")
    print(f"Total cost:             {FV.FDollar2(TotalCost)}")

    if CustPayPlan != "Full":
        print(f"Monthly payment:          {FV.FDollar2(MonthlyPayment)}")
    print()
    print(f"First Payment Due: {LongDate(FirstPaymentDate)}")
    print("==================================================================")
    print()
    print()
    print("Claim Information")
    print("==================================================================")

    print("Claim #   Claim Date       Amount")
    print("---------------------------------")
    for i in range(len(ClaimNumbers)):
        print(f"{ClaimNumbers[i]:<4}      {FV.FDateS(ClaimDates[i])}    {FV.FDollar2(ClaimAmounts[i])}")
    print()
    print(f"Total previous claim amount: {FV.FDollar2(TotalPrevClaimAmt)}")
    print("==================================================================")


    #Update Counters/Write to data files 

    f = open("PolicyData.dat", "a")
    f.write(f"{POLICY_NUM}, {CustFirstName}, {CustSurname}, {CustAddress}, {CustomerCity},{CustomerProvince},{CustomerPostal},{CustomerPhone},{NumCarsIns},{ExtraLiab},{OptionalGlass},{LoanerCar},{CustPayPlan},{TotalPremium:.2f},{HST:.2f},{TotalCost:.2f},{TotalPrevClaimAmt:.2f}\n")
    for i in range(len(ClaimNumbers)):
        f.write(f"{POLICY_NUM},{ClaimNumbers[i]},{ClaimDates[i]},{ClaimAmounts[i]:.2f}\n")
    f.close()

    POLICY_NUM += 1

    f = open("Const.dat", "w")
    f.write(f"{POLICY_NUM}, {BASIC_PREMIUM}, {ADD_CAR_DISCOUNT}, {EXTRA_LIAB_COST}, {GLASS_COST}, {LOANER_COVERAGE}, {HST_RATE}, {MONTHLY_PROC}\n")
    f.close()

    RepeatProcess = input("Would you like to enter another policy into the system? (Y/N): ").strip().upper()
    if RepeatProcess == "N":
        break


