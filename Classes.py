import Variables
import pandas as pd
class record:
    source = ""
    TransactionDate=""
    Day=0
    Month = 0
    Year = 0
    ValueHUF = 0.0

    def __init__(self,v,src,dat):
        self.source = src
        self.type="" # Expense Type
        self.ValueHUF = v
        self.TransactionDate = dat
        self.translatedates(dat)
        
    def translatedates (self,dat):
        self.Day = dat[0]
        self.Month = dat[1]-1
        self.Year = dat[2]

    def Printout (self):
        print(self.source,"\t",self.ValueHUF,"\t",self.TransactionDate,"\t",self.type)

class MonthlySummary:

    def __init__(self,month,year):
        self.Month = month
        self.Year = year
        self.TotalRecords=[]
        self.SortedRecords=[[] for _ in range(len(Variables.RecordTypes))]
        self.SortedSums=[]
        self.TotalSum=0
        self.SourceType = []
        self.MaxRecNumber=0

    def printout(self):
        for i in self.TotalRecords:
            i.printout()
    def SortRecordsTypewise (self):
        for rec in self.TotalRecords:
            for idx,Type in enumerate(Variables.RecordTypes):
                if rec.type == Type:
                    self.SortedRecords[idx].append(rec)
    
    def CalculateRecordStats(self):
        for group in self.SortedRecords:
            Groupsum=0

            if len(group)>self.MaxRecNumber:
                self.MaxRecNumber=len(group)

            for rec in group:
                Groupsum= Groupsum + rec.ValueHUF
            self.SortedSums.append(Groupsum)
        self.TotalSum=sum(self.SortedSums)
              
class statement:
    path=""
    Records=[]
    TotalYears=[]
    YearlySummaryList=[]#Container for sorted records
    def __init__(self,Empty=False):
        self.UnknownRecords= [] # List of unknown Records for debugging
        self.YearlySummaryList=[[] for _ in range(len(Variables.TotalYears))]
        self.TotalYears=Variables.TotalYears
        if not Empty:  
            self.AssignRecordType()
            self.InitializeYearlySummaryList()
            self.SortRecordsTimewise()
            self.SortRecordsTypewise()
            self.CalculateStatementStats()

    def readstatement():
        pass 
    def InitializeYearlySummaryList(self) :
        for idx,YearlySummary in enumerate(self.YearlySummaryList):
            for MonthNo  in  range(0,12):
                 YearlySummary.append(MonthlySummary(MonthNo,self.TotalYears[idx]))
    
    def SortRecordsTimewise(self):
        for Record in self.Records:
            for idx,Year in enumerate(self.TotalYears):
                if(Record.Year==Year):
                    self.YearlySummaryList[idx][Record.Month].TotalRecords.append(Record)

    def AssignRecordType (self):
        for rec in self.Records:
            for idx,exptype in enumerate(Variables.KnownSources):
                for detailedtype in exptype:
                    if detailedtype.lower() in rec.source.lower() :
                        rec.type = Variables.RecordTypes[idx]

        for rec in self.Records:
            if rec.type == "":
                rec.type = "Unknown" 
                self.UnknownRecords.append(rec)   
    def SortRecordsTypewise(self):# Possible name conflict with MonthlySummary
        for year in self.YearlySummaryList:
            for month in year:  
                month.SortRecordsTypewise()

    def CalculateStatementStats(self):
        for year in self.YearlySummaryList:
            for month in year:
                month.CalculateRecordStats()            

class UnicreditStatement (statement):
    
    def __init__(self,path):
        self.Records=[]
        self.path=path
        self.readstatement()
        super().__init__()
        

    def readstatement(self):
        Cost=[]
        df = pd.read_excel(self.path,'export',skiprows=[0,1,2],converters={'Amount':str,'Value Date':str,'Partner':str})
        Value=df["Amount"].astype(str).values.tolist()
        Source=df["Partner"].astype(str).values.tolist()
        Date=df["Value Date"].astype(str).values.tolist()

        for val in Value: #Prepare cost -> To be added with many Currencies
            temp1=val.strip(" ,HUF")
            temp2=temp1.replace(".00","")
            temp=temp2.replace(",","")
            Cost.append(float(temp))

        self.Values=Cost
        self.Sources=Source
        self.Dates = Date

        # FOR DYNAMIC YEARS
        # for count in range(0,len(self.Values)-1):
        #     temprec=record(self.Values[count] , self.Sources[count] , self.DateToInt(self.Dates[count]))
        #     if not temprec.Year in Variables.TotalYears:
        #         Variables.TotalYears.append(temprec.Year)
        #     self.Records.append(temprec)
        # Variables.TotalYears.sort()
        
        for count in range(0,len(self.Values)-1):
            temprec=record(self.Values[count] , self.Sources[count] , self.DateToInt(self.Dates[count]))
            self.Records.append(temprec)
        

    def DateToInt (self,Rawdate):
        Day=int(Rawdate[0]+Rawdate[1])
        Month=int(Rawdate[3]+Rawdate[4])
        Year=int(Rawdate[6]+Rawdate[7]+Rawdate[8]+Rawdate[9])
        ret=[]
        ret.append(Day)
        ret.append(Month)
        ret.append(Year)
        return (ret)

class RevolutStatement (statement): # In HUF
    
    def __init__(self,path):
        self.Records=[]
        self.path=path
        self.readstatement()
        super().__init__()
        

    def readstatement(self):
        Cost=[]
        df = pd.read_csv(self.path)
        Value=df["Amount"].astype(str).values.tolist()
        Source=df["Description"].astype(str).values.tolist()
        Date=df["Started Date"].astype(str).values.tolist()

        for val in Value: #Prepare cost -> To be added with many Currencies
            temp1=val.strip(" ,HUF")
            temp2=temp1.replace(".00","")
            temp=temp2.replace(",","")
            Cost.append(self.TransferToHUF(float(temp)))
            #Cost.append(float(temp)*Variables.PLNHUF) # Translated to HUF

        self.Values=Cost
        self.Sources=Source
        self.Dates = Date

        for count in range(0,len(self.Values)-1):
            temprec=record(self.Values[count] , self.Sources[count] , self.DateToInt(self.Dates[count]))
            self.Records.append(temprec)

    def TransferToHUF (self,value): # Abstract, default for huf
        #return float(value)*Variables.PLNHUF
        return value


    def DateToInt (self,Rawdate):
        Year=int(Rawdate[0]+Rawdate[1]+Rawdate[2]+Rawdate[3])
        Month=int(Rawdate[5]+Rawdate[6])
        Day=int(Rawdate[8]+Rawdate[9])
        ret=[]
        ret.append(Day)
        ret.append(Month)
        ret.append(Year)
        return (ret)



        #  def TransferToHUF (self,value):
        # return float(value)*Variables.PLNHUF+
class RevolutPLN(RevolutStatement):
    def __init__(self, path):
        super().__init__(path)

    def TransferToHUF (self,value): # Abstract
        return float(value)*Variables.PLNHUF
    
class RevolutEUR(RevolutStatement):
    def __init__(self, path):
        super().__init__(path)

    def TransferToHUF (self,value): # Abstract
        return float(value)*Variables.EURHUF

class RevolutHRK(RevolutStatement):
    def __init__(self, path):
        super().__init__(path)

    def TransferToHUF (self,value): # Abstract
        return float(value)*Variables.HRKHUF