from Classes import *
from FunDeclare import *
from Variables import *
fname="Revolut"
temp=0
#Read Expense types
RecordTypes,KnownSources = readExpenseTypes (ListPath)
Variables.RecordTypes = RecordTypes
Variables.KnownSources = KnownSources
#Handle Unicredit Statement
#Unicredit = UnicreditStatement(Variables.UnicreditPath)
#Handle Revolut Statement
###RHUF=RevolutStatement(Variables.RevolutHUFpath)
###RPLN=RevolutPLN(Variables.RevolutPLNpath)
RHRK=RevolutHRK(Variables.RevolutHRKpath)
###REUR=RevolutEUR(Variables.RevolutEURpath)

#StatementsToServe=[Unicredit,RHUF,RPLN,RHRK,REUR] # For all statements
StatementsToServe=[RHRK]  #Fake data to demonstrate Capabilities
#Create Merged Statement
GlobalStatement=statement(True)
# Write to EXCEL

MergeStatements(GlobalStatement,StatementsToServe)

WriteToExcel(GlobalStatement,"Global")

for s in StatementsToServe: 
    for rec in s.UnknownRecords:
        rec.Printout()
        temp=temp+1

print(temp)