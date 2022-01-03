import pandas as pd
from Variables import *
from Classes import*
import xlsxwriter
import calendar

def readExpenseTypes(fpath):
    df = pd.read_excel(fpath)
    Sources= [] #Data of the sources
    RecordTypeGroups=list(df) #List oif the source type
    for idx in RecordTypeGroups:
        DetailedTypes=df[idx].astype(str).values.tolist()
        temp = [x for x in DetailedTypes if x != 'nan'] #Removes nans
        if idx == "Unknown":
            temp.append("nan")
        Sources.append(temp)
    return  RecordTypeGroups,Sources


def WriteToExcel(Statement,fname):
    for Yidx,year in enumerate(Variables.TotalYears):
        workbook = xlsxwriter.Workbook(f"ExpenseSummary\\{fname}{year}.xlsx")


        for idx,Monthlydata in enumerate(Statement.YearlySummaryList[Yidx]):
            worksheet = workbook.add_worksheet(calendar.month_abbr[idx+1])
            row = 0
            col = 0
            for Type in Variables.RecordTypes:
                worksheet.write(0,col,Type)
                col=col+2

            for idx,reclist in enumerate(Monthlydata.SortedRecords):
                row=1
                for rec in reclist:
                    worksheet.write(row,idx*2,rec.source)
                    worksheet.write(row,idx*2+1,rec.ValueHUF)
                    row=row + 1
            col=1
            for sum in Monthlydata.SortedSums:
                worksheet.write(Monthlydata.MaxRecNumber+1,col,sum)
                col=col+2  

            worksheet.write(Monthlydata.MaxRecNumber+2,col,Monthlydata.TotalSum)

        worksheet = workbook.add_worksheet("Yearly Summary")
        col=0
        for Type in Variables.RecordTypes:
            worksheet.write(0,col,Type)
            col=col+1
        worksheet.write(0,col,"Total Summary")
        for idx,Monthlydata in enumerate(Statement.YearlySummaryList[Yidx]):
            col=0
            for sum in Monthlydata.SortedSums:
                worksheet.write(idx+2,col,sum)
                col=col+1
            worksheet.write(idx+2,col,Monthlydata.TotalSum)

        
        workbook.close()

def MergeStatements(GlobalStatement,Statements): 
    
    for Stat in Statements:
        GlobalStatement.Records=GlobalStatement.Records+Stat.Records
    GlobalStatement.AssignRecordType()
    GlobalStatement.InitializeYearlySummaryList()
    GlobalStatement.SortRecordsTimewise()
    GlobalStatement.SortRecordsTypewise()
    GlobalStatement.CalculateStatementStats()
    return GlobalStatement


