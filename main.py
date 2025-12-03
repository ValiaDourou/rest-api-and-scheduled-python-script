
import PyPDF2
import re
import json
import requests
from bs4 import BeautifulSoup
import calendar
import logging
import logging.handlers
import os
import datetime

import requests



def extract_from_pdf(program,filename):

 # Choose pdf file
 pdfFile = open(program, "rb")
 
 # Create an object for reading the file
 pdfReader = PyPDF2.PdfReader(pdfFile)
 
 # Get the number of pages
 numPages = len(pdfReader.pages)
 
 text=''
 # Create an object to get the text from each page
 for i in range(numPages):
    page = pdfReader.pages[i]
    text= text + page.extract_text()

 t=text.strip()

 t=t.split('ΠΡΟΣΦΕΡΟΜΕΝΟ')
 # Filter out ΝΗΣΤΙΣΙΜΕΣ ΕΠΙΛΟΓΕΣ (fasting options) sections - only keep ΒΕΛΤΙΩΜΕΝΟ ΕΔΕΣΜΑΤΟΛΟΓΙΟ sections
 finalt=[section for section in t[1:len(t)] if 'ΝΗΣΤΙΣΙΜΕΣ' not in section and 'ΒΕΛΤΙΩΜΕΝΟ' in section]

 lunch=[]
 dinner=[]
 breakfast=[]
 dates=[]
 firstDishes=[]
 mainDishes1=[]
 mainDishes2=[]
 sideDishes=[]
 dessertL=[]
 lunchDesserts=[]
 DfirstDishes=[]
 DmainDishes1=[]
 DmainDishes2=[]
 DsideDishes=[]
 DdessertL=[]
 dinnerDesserts=[]
 cnt=0
 v=0
 s=0
 fc=0
 fcd=0
 sd=0
 cntd=0

 for i in finalt:
    week=i.split('ΔΕΙΠΝΟ')
    lunch=week[0]
    dinner=week[1]

    if i==finalt[-1]:
        breakfast=re.split('ΠΡΩΙΝΟ|Πρωινό',dinner)[1]
        dinner=re.split('ΠΡΩΙΝΟ|Πρωινό',dinner)[0]
        

    #Get the dates
    datesW=re.split('Πρώτο',lunch)[0]
    datesl=re.split('ΓΕΥΜΑ',datesW)[1]

    #All the dates from the pdf are now in a list
    datesl=re.split('Κυριακή |Δευτέρα |Τρίτη |Τετάρτη |Πέμπτη |Παρασκευή |Σάββατο',datesl)
    datesl=list(map(str.strip, datesl[1:]))
    dates=dates+datesl

    #Get the first dish
    firstD=re.split('Πρώτο[\s]*[\n]*[\s]*Πιάτο|Πρώτο[\s]*[\n]*[\s]*πιάτο',lunch)[1]
    firstD=re.split('Κυρίως',firstD)[0]

    #All the first dishes from the pdf are now in a list
    x=re.search('Σεφ',firstD)

    if x!='None':
        firstD = re.sub("Σεφ", "σεφ", firstD)
    firstD=re.split('([Α-Ω])',firstD)
    firstD=list(map(str.strip, firstD[1:]))
    firstD = [s.replace('\n', '') for s in firstD]
    i=0
    for i in range(len(firstD)-1):
        firstD[i]=firstD[i]+firstD[i+1]


    firstDishesl = [v for i, v in enumerate(firstD) if i % 2 == 0]
    firstDishes=firstDishes+firstDishesl

    #Get the first main dish
    mainD1=re.split('Πιάτα [\n]*1',lunch)[1]
    mainD1=re.split('2',mainD1)[0]

    #All the first main dishes from the pdf are now in a list
    x=re.search('Βολιώτικο',mainD1)
    y=re.search('Μπότσαρη',mainD1)
    z=re.search('Λαχανικών',mainD1)
    w=re.search('Τυρί',mainD1)
    j=re.search('Τριμμένο',mainD1)

    if x!='None':
        mainD1 = re.sub("Βολιώτικο", "βολιώτικο", mainD1)
    if y!='None':
        mainD1 = re.sub("Μπότσαρη", "μπότσαρη", mainD1)
    if z!='None':
        mainD1 = re.sub("Λαχανικών", "λαχανικών", mainD1)
    if w!='None':
        mainD1 = re.sub("Τυρί", "τυρί", mainD1)
    if j!='None':

        mainD1 = re.sub("Τριμμένο", "τριμμένο", mainD1)
    mainD1=re.split('([Α-Ω])',mainD1)
    mainD1=list(map(str.strip, mainD1[1:]))
    mainD1 = [s.replace('\n', '') for s in mainD1]
    i=0
    for i in range(len(mainD1)-1):
        mainD1[i]=mainD1[i]+mainD1[i+1]

    mainDishes1l = [v for i, v in enumerate(mainD1) if i % 2 == 0]
    for e in mainDishes1l:
     r=re.search('Κυρίως',e)
     if r is not None:
        mainDishes1l.remove('Κυρίως')
        mainDishes1l.remove('Πιάτα')
    mainDishes1=mainDishes1+mainDishes1l

    #Get the second main dish
    mainD2=re.split('Πιάτα [\n]*1',lunch)[1]
    mainD2=re.split('2',mainD2)[1]
    if 'Μπουφές Σαλάτα' in lunch:
        mainD2=re.split('Μπουφές Σαλάτα',mainD2)[0]
    else:
        if 'Συνοδευτικά' in lunch:
            mainD2=re.split('Συνοδευτικά',mainD2)[0]
        elif 'Μαρούλι' in lunch:
            mainD2=re.split('Μαρούλι',mainD2)[0]
        elif 'Λάχανο' in lunch:
            mainD2=re.split('Λάχανο',mainD2)[0]
        elif 'Μπρόκολο' in lunch:
            mainD2=re.split('Μπρόκολο',mainD2)[0]
        elif 'Κουνουπίδι' in lunch:
            mainD2=re.split('Κουνουπίδι',mainD2)[0]
        elif 'Ταραμοσαλάτα' in lunch:
            mainD2=re.split('Ταραμοσαλάτα',mainD2)[0]
    
    #All the second main dishes from the pdf are now in a list
    x=re.search('Βολιώτικο',mainD2)
    y=re.search('Μπότσαρη',mainD2)
    z=re.search('Λαχανικών',mainD2)
    w=re.search('Τυρί',mainD2)
    j=re.search('Τριμμένο',mainD2)

    if x!='None':
        mainD2 = re.sub("Βολιώτικο", "βολιώτικο", mainD2)
    if y!='None':
        mainD2 = re.sub("Μπότσαρη", "μπότσαρη", mainD2)
    if z!='None':
        mainD2 = re.sub("Λαχανικών", "λαχανικών", mainD2)
    if w!='None':
        mainD2 = re.sub("Τυρί", "τυρί", mainD2)
    if j!='None':
        mainD2 = re.sub("Τριμμένο", "τριμμένο", mainD2)
    mainD2=re.split('([Α-Ω])',mainD2)
    mainD2=list(map(str.strip, mainD2[1:]))
    mainD2 = [s.replace('\n', '') for s in mainD2]
    i=0
    for i in range(len(mainD2)-1):
        mainD2[i]=mainD2[i]+mainD2[i+1]

    mainDishes2l = [v for i, v in enumerate(mainD2) if i % 2 == 0]
    
    for e in mainDishes2l:
     r=re.search('Συνοδευτικά',e)
     if r is not None:
        mainDishes2l.remove('Συνοδευτικά')
    mainDishes2=mainDishes2+mainDishes2l

    #Get the side dish
    if 'Μπουφές Σαλάτα' in lunch:
        side=re.split('Μπουφές Σαλάτα',lunch)[1]
        side=re.split('Επιδόρπιο',side)[0]
    else:
        if 'Συνοδευτικά' in lunch:
            side=re.split('Συνοδευτικά',lunch)[1]
        elif 'Μαρούλι' in lunch:
            side='Μαρούλι' + re.split('Μαρούλι',lunch,1)[1]
        elif 'Λάχανο' in lunch:
            side='Λάχανο' + re.split('Λάχανο',lunch,1)[1]
        elif 'Μπρόκολο' in lunch:
            side='Μπρόκολο' + re.split('Μπρόκολο',lunch,1)[1]
        elif 'Κουνουπίδι' in lunch:
            side='Κουνουπίδι' + re.split('Κουνουπίδι',lunch,1)[1]
        elif 'Ταραμοσαλάτα' in lunch:
            side='Ταραμοσαλάτα' + re.split('Ταραμοσαλάτα',lunch,1)[1]
        side=re.split('Φρούτο',side, 1)[0]

    #All the side dishes from the pdf are now in a list
    x=re.search('Λάχανο',side)
    y=re.search(',[\s]*Μαρούλι',side)
    w=re.search('Φλωρίνης',side)

    if x!='None':
        side = re.sub("Λάχανο", "λάχανο", side)
    # if y!='None':
    #     side = re.sub(',[\s]*Μαρούλι',',μαρούλι', side)
    if w!='None':
        side = re.sub('Φλωρίνης','φλωρίνης', side)

    side=re.split('([Α-Ω])',side)
    side=list(map(str.strip, side[1:]))
    side = [s.replace('\n', '') for s in side]
    i=0
    for i in range(len(side)-1):
        side[i]=side[i]+side[i+1]

    sidel = [v for i, v in enumerate(side) if i % 2 == 0]
    sideDishes=sideDishes+sidel

    #Get the dessert 
    if 'Μπουφές Σαλάτα' in lunch:
        dessert=re.split('Επιδόρπιο',lunch)[1]
    else:
        if 'Συνοδευτικά' in lunch:
            dessert=re.split('Συνοδευτικά',lunch)[1]
            dessert=re.split('2[\s]*[\n]*επιλογές[\s]*',dessert,1)[1]

        else:
            dessert = re.split('επιλογές', lunch)[7]
    
    #All the desserts from the pdf are now in a list
    x=re.search('-[\s]*Γλυκό',dessert)

    if x!='None':
        dessert = re.sub("-[\s]*Γλυκό", "-γλυκό", dessert)
    dessert=re.split('([\s]*[Α-ΔΖ-ΥΧ-Ω])',dessert)
    dessert=list(map(str, dessert[1:]))

    i=0
    for i in range(len(dessert)-1):
        dessert[i]=dessert[i]+dessert[i+1]        

    dessertl = [v for i, v in enumerate(dessert) if i % 2 == 0]

    rd=0
    if v==0:
     for h in range(len(dessertl)):
       if h==len(dessertl)-1:
        p=re.split('\n',dessertl[h])[0]
        rd=(len(p)-len(p.rstrip())-1) / 2
    
    if len(dessertl)>0:
      dessertl[len(dessertl)-1]=dessertl[len(dessertl)-1].rstrip()
    

    dessertl = [re.sub('\n', '!',s) for s in dessertl]
    if v==0:
     st=dessertl
     cnt=len(dates)-len(st)
     if cnt==len(dates):
      s=len(dates)
      fc=7
     if len(dates)==7:
      s=0
      fc=7
     if len(dates)!=7 and cnt>0 and cnt!=len(dates):
      ldiff=0
      rdiff=rd
      for h in range(1,len(st)):
       ldiff=ldiff+len(st[h])-len(st[h].lstrip())-1
      s=cnt-ldiff
      sl=re.split('!',st[0])[1]
      fd=len(sl)-len(sl.lstrip())
      dd=7-len(dates)
      g=len(dates)-len(st)-rdiff
      if fd>dd:
        s=s-1
      if g==0:
        s=0
      fc=len(dates)
    dessertL=dessertL+dessertl

    ######################################################################################################################

    #Get dinner info
    #Get the first dish
    DfirstD=re.split('Πρώτο[\s]*[\n]*[\s]*Πιάτο|Πρώτο[\s]*[\n]*[\s]*πιάτο',dinner)[1]
    DfirstD=re.split('Κυρίως',DfirstD)[0]

    w=re.search('Σεφ',DfirstD)
    x=re.search('Ζυμαρικών',DfirstD)
    y=re.search('Φρανκφούρτης',DfirstD)

    if w!='None':
        DfirstD = re.sub("Σεφ", "σεφ", DfirstD)
    if x!='None':
        DfirstD = re.sub("Ζυμαρικών", "ζυμαρικών", DfirstD)
    if y!='None':
        DfirstD = re.sub("Φρανκφούρτης", "φρανκφούρτης", DfirstD)

    #All the first dishes from the pdf are now in a list
    DfirstD=re.split('([Α-Ω])',DfirstD)
    DfirstD=list(map(str.strip, DfirstD[1:]))
    DfirstD = [s.replace('\n', '') for s in DfirstD]
    i=0
    for i in range(len(DfirstD)-1):
        DfirstD[i]=DfirstD[i]+DfirstD[i+1]

    DfirstDishesl = [v for i, v in enumerate(DfirstD) if i % 2 == 0]
    DfirstDishes=DfirstDishes+DfirstDishesl

    #Get the first main dish
    DmainD1=re.split('Πιάτα [\n]*1',dinner)[1]
    DmainD1=re.split('2',DmainD1)[0]

    #All the first main dishes from the pdf are now in a list
    x=re.search('Βολιώτικο',DmainD1)
    y=re.search('Μπότσαρη',DmainD1)
    z=re.search('Λαχανικών',DmainD1)
    w=re.search('Τυρί',DmainD1)
    j=re.search('Τριμμένο',DmainD1)

    if x!='None':
        DmainD1 = re.sub("Βολιώτικο", "βολιώτικο", DmainD1)
    if y!='None':
        DmainD1 = re.sub("Μπότσαρη", "μπότσαρη", DmainD1)
    if z!='None':
        DmainD1 = re.sub("Λαχανικών", "λαχανικών", DmainD1)
    if w!='None':
        DmainD1 = re.sub("Τυρί", "τυρί", DmainD1)
    if j!='None':

        DmainD1 = re.sub("Τριμμένο", "τριμμένο", DmainD1)
    DmainD1=re.split('([Α-Ω])',DmainD1)
    DmainD1=list(map(str.strip, DmainD1[1:]))
    DmainD1 = [s.replace('\n', '') for s in DmainD1]
    i=0
    for i in range(len(DmainD1)-1):
        DmainD1[i]=DmainD1[i]+DmainD1[i+1]

    DmainDishes1l = [v for i, v in enumerate(DmainD1) if i % 2 == 0]
    for e in DmainDishes1l:
     r=re.search('Κυρίως',e)
     if r is not None:
        DmainDishes1l.remove('Κυρίως')
        DmainDishes1l.remove('Πιάτα')


    DmainDishes1=DmainDishes1+DmainDishes1l

    #Get the second main dish
    DmainD2=re.split('Πιάτα [\n]*1',dinner)[1]
    DmainD2=re.split('2',DmainD2)[1]
    if 'Συνοδευτικά' in dinner:
        DmainD2=re.split('Συνοδευτικά',DmainD2)[0]
    if 'Μπουφές Σαλάτα' in dinner and 'Συνοδευτικά' not in dinner:
        DmainD2=re.split('Μπουφές Σαλάτα',DmainD2)[0]
    if 'Μπουφές Σαλάτα' not in dinner and 'Συνοδευτικά' not in dinner:
        DmainD2=re.split('Μαρούλι',DmainD2)[0]

    
    #All the second main dishes from the pdf are now in a list
    x=re.search('Βολιώτικο',DmainD2)
    y=re.search('Μπότσαρη',DmainD2)
    z=re.search('Λαχανικών',DmainD2)
    w=re.search('Τυρί',DmainD2)
    j=re.search('Τριμμένο',DmainD2)
    p=re.search('Ριζότο',DmainD2)

    if x!='None':
        DmainD2 = re.sub("Βολιώτικο", "βολιώτικο", DmainD2)
    if y!='None':
        DmainD2 = re.sub("Μπότσαρη", "μπότσαρη", DmainD2)
    if z!='None':
        DmainD2 = re.sub("Λαχανικών", "λαχανικών", DmainD2)
    if w!='None':
        DmainD2 = re.sub("Τυρί", "τυρί", DmainD2)
    if j!='None':
        DmainD2 = re.sub("Τριμμένο", "τριμμένο", DmainD2)
    if p!='None':
        DmainD2 = re.sub("Ριζότο", "ριζότο", DmainD2)
    DmainD2=re.split('([Α-Ω])',DmainD2)
    DmainD2=list(map(str.strip, DmainD2[1:]))
    DmainD2 = [s.replace('\n', '') for s in DmainD2]
    i=0
    for i in range(len(DmainD2)-1):
        DmainD2[i]=DmainD2[i]+DmainD2[i+1]

    DmainDishes2l = [v for i, v in enumerate(DmainD2) if i % 2 == 0]
    for e in DmainDishes2l:
     r=re.search('Συνοδευτικά',e)
     if r is not None:
        DmainDishes2l.remove('Συνοδευτικά')
    DmainDishes2=DmainDishes2+DmainDishes2l

    #Get the side dish
    if 'Μπουφές Σαλάτα' in dinner:
        Dside=re.split('Μπουφές Σαλάτα',dinner)[1]
        Dside=re.split('Επιδόρπιο|ΕΠΙΔΟΡΠΙ O',Dside)[0]
    if 'Μπουφές Σαλάτα' in dinner and ('Επιδόρπιο' in dinner or 'ΕΠΙΔΟΡΠΙ O' in dinner):
        Dside=re.split('Μπουφές Σαλάτα',dinner)[1]
        Dside=re.split('Επιδόρπιο|ΕΠΙΔΟΡΠΙ O',Dside)[0]
    if 'Μπουφές Σαλάτα' in dinner and ('Επιδόρπιο' not in dinner and 'ΕΠΙΔΟΡΠΙ O' not in dinner):
        Dside=re.split('Μπουφές Σαλάτα',dinner)[1]
        Dside=re.split('Φρούτο',Dside)[0]
    if 'Μπουφές Σαλάτα' not in dinner and 'Συνοδευτικά' in dinner:
        Dside=re.split('Συνοδευτικά',dinner)[1]
        Dside=re.split('Φρούτο',Dside)[0]
    if 'Μπουφές Σαλάτα' not in dinner and 'Συνοδευτικά' not in dinner:
        Dside=re.split('τριμμένο',dinner)[1]
        Dside=re.split('Επιδόρπιο',Dside)[0]        

    #All the side dishes from the pdf are now in a list
    x=re.search('Λάχανο',Dside)
    r=re.search('κόκκινο, Μαρούλι',Dside)
    if r is not None:
        Dside=re.sub('κόκκινο, Μαρούλι','κόκκινο Μαρούλι',Dside)
    y=re.search(',[\s]*Μαρούλι',Dside)
    w=re.search('Φλωρίνης',Dside)
    if x!='None':
        Dside = re.sub("Λάχανο", "λάχανο", Dside)
    if y!='None':
        Dside = re.sub(',[\s]*Μαρούλι',',μαρούλι', Dside)
    if w!='None':
        Dside = re.sub('Φλωρίνης','φλωρίνης', Dside)

    Dside=re.split('([Α-Ω])',Dside)
    Dside=list(map(str.strip, Dside[1:]))
    Dside = [s.replace('\n', '') for s in Dside]
    i=0
    for i in range(len(Dside)-1):
        Dside[i]=Dside[i]+Dside[i+1]

    Dsidel = [v for i, v in enumerate(Dside) if i % 2 == 0]
    DsideDishes=DsideDishes+Dsidel

    #Get the dessert 
    if 'Μπουφές Σαλάτα' in dinner:
        if 'Επιδόρπιο' in dinner or 'ΕΠΙΔΟΡΠΙ O' in dinner:
            Ddessert=re.split('Επιδόρπιο|ΕΠΙΔΟΡΠΙ O',dinner)[1]
        else:
            Ddessert=re.split('2[\s]*[\n]*επιλογές[\s]*',dinner,1)[1]
    else:
        if 'Συνοδευτικά' in dinner:
            Ddessert=re.split('Συνοδευτικά',dinner)[1]
            Ddessert=re.split('2[\s]*[\n]*επιλογές[\s]*',Ddessert,1)[1]

        else:
            Ddessert = re.split('επιλογές', dinner)[7]
    
    #All the desserts from the pdf are now in a list
    x=re.search('-[\s]*Γλυκό',Ddessert)

    if x!='None':
        Ddessert = re.sub("-[\s]*Γλυκό", "-γλυκό", Ddessert)
    Ddessert=re.split('([\s]*[Α-ΔΖ-ΥΧ-Ω])',Ddessert)
    Ddessert=list(map(str, Ddessert[1:]))

    i=0
    for i in range(len(Ddessert)-1):
        Ddessert[i]=Ddessert[i]+Ddessert[i+1]        

    Ddessertl = [v for i, v in enumerate(Ddessert) if i % 2 == 0]
    Drd=0
    if v==0:
     for h in range(len(Ddessertl)):
       if h==len(Ddessertl)-1:
        p=re.split('\n',Ddessertl[h])[0]
        Drd=(len(p)-len(p.rstrip())-1) / 2
    if len(Ddessertl)>0:
      Ddessertl[len(Ddessertl)-1]=Ddessertl[len(Ddessertl)-1].rstrip()
    Ddessertl = [re.sub('[\t\n ]*\*Ειδικό πιάτο : Aφορά ειδικές διατροφικές ανάγκες και προσδιορίζεται κάθε φορά μετά από καταγραφή της σχετικής ανάγκης.[\t]*[\n]*', '',s) for s in Ddessertl]
    Ddessertl = [re.sub('[\t\n ]*\*Ειδικό πιάτο : Aφορά ειδικές διατροφικές ανάγκες και προσδιορίζεται κάθε φορά μετά από καταγραφή της σχετικής ανάγκης[\t]*[\n]*', '',s) for s in Ddessertl]
    
    if Ddessertl and '\n' not in Ddessertl[0]:
        Ddessertl[0] = '\n'+Ddessertl[0]

    Ddessertl = [re.sub('\n', '!',s) for s in Ddessertl]

    if v==0:
     st=Ddessertl
     cnt=len(dates)-len(st)
     if cnt==len(dates):
      sd=len(dates)
      fcd=7
     if len(dates)==7:
      sd=0
      fcd=7
     if len(dates)!=7 and cnt>0 and cnt!=len(dates):
      ldiff=0
      rdiff=Drd
      for h in range(1,len(st)):
       ldiff=ldiff+len(st[h])-len(st[h].lstrip())-1
      sd=cnt-ldiff
      sl=re.split('!',st[0])[1]
      fdd=len(sl)-len(sl.lstrip())
      dd=7-len(dates)
      g=len(dates)-len(st)-rdiff
      if fd>dd:
        sd=sd-1
      if g==0:
        sd=0
      fcd=len(dates)
    v=v+1
    DdessertL=DdessertL+Ddessertl 

 l=[]
 lD=[]
 for b in dessertL:
    if '!' in b:
      a=re.split('!',b)[1]
      y=len(a)-len(a.lstrip())
      l.append(y)

 for b in DdessertL:
    if '!' in b:
      a=re.split('!',b)[1]
      y=len(a)-len(a.lstrip())
      lD.append(y) 
 
 dessertfL= [re.sub('[\s]*!', '',s) for s in dessertL]
 counter=0
 r=0
 z=0
 for i in range(s):
   lunchDesserts.append('-')
 if fc<7:
  for i in range(len(dessertL)):
    c=re.search('!',dessertL[i])

    if c!=None:
        if counter<=7 and counter>0 and r>0:
            cd=7-counter
            for j in range(cd):
                lunchDesserts.append('-')
            counter=0
            r=r+1
        if counter<=fc and counter>0 and r==0:
            cd=fc-counter
            for j in range(cd):
                lunchDesserts.append('-')
            counter=0
            r=r+1
    if counter==0 and r>0:
     for j in range(l[r]):
        lunchDesserts.append('-')
        counter=counter+1

     z=1
     counter=counter+1
     
    if counter==0 and i==0:
     counter=counter+1+s
            
    diff=len(dessertfL[i])-len(dessertfL[i].lstrip())

    if z==0 and i!=0:
     for k in range(diff-1):
        lunchDesserts.append('-')
     counter=counter+diff

    lunchDesserts.append(dessertfL[i].strip())
    z=0
    if counter>=7 and r>0:
        counter=0
        r=r+1
    if counter>=fc and r==0:
        counter=0
        r=r+1
 if fc==7:
    for i in range(len(dessertL)):
     c=re.search('!',dessertL[i])
     if c!=None:
        if counter>0 and counter<7:
            cd=7-counter
            for k in range(cd):
                lunchDesserts.append('-')
            counter=0
            r=r+1

     if counter!=0:
      diff=len(dessertfL[i])-len(dessertfL[i].lstrip())
      for k in range(diff-1):
         lunchDesserts.append('-')
         counter=counter+1
     if counter==0 and r>0:
      if l[r]>0:
       for j in range(l[r]):
        lunchDesserts.append('-')
        counter=counter+1
     if counter==0 and r==0:
        diff=len(dessertfL[i])-len(dessertfL[i].lstrip())
        for k in range(diff):
         lunchDesserts.append('-')
         counter=counter+1

     lunchDesserts.append(dessertfL[i].strip())
     counter=counter+1
     if counter>=7:
        counter=0
        r=r+1

 if len(lunchDesserts)<len(dates):
    d=len(dates)-len(lunchDesserts)
    for j in range(d):
        lunchDesserts.append('-')

 #Dinner desserts
 DdessertfL= [re.sub('[\s]*!', '',s) for s in DdessertL]
 counterD=0
 rD=0
 zD=0
 for i in range(sd):
  dinnerDesserts.append('-')
 if fcd<7:
  for i in range(len(DdessertL)):
    c=re.search('!',DdessertL[i])

    if c!=None:
        if counterD<=7 and counterD>0 and rD>0:
            cd=7-counterD
            for j in range(cd):
                dinnerDesserts.append('-')
            counterD=0
            rD=rD+1
        if counterD<=fcd and counterD>0 and rD==0:
            cd=fcd-counterD
            for j in range(cd):
                dinnerDesserts.append('-')
            counterD=0
            rD=rD+1
    if counterD==0 and rD>0:
     for j in range(lD[rD]):
        dinnerDesserts.append('-')
        counterD=counterD+1
     zD=1
     counterD=counterD+1
    if counterD==0 and i==0 and DdessertL[i+1] and i < len(DdessertL) and re.search('!',DdessertL[i+1]) != None:
     counterD=counterD+1+sd
            
    diff=len(DdessertfL[i])-len(DdessertfL[i].lstrip())

    if zD==0 and i!=0:
     for k in range(diff-1):
        dinnerDesserts.append('-')
     counterD=counterD+diff

    dinnerDesserts.append(DdessertfL[i].strip())
    zD=0
    if counterD>=7 and rD>0:
        counterD=0
        rD=rD+1
    if counterD>=fcd and rD==0 and i < len(DdessertL) and re.search('!',DdessertL[i+1]) != None:
        counterD=0
        rD=rD+1
 if fcd==7:
    for i in range(len(DdessertL)):
     c=re.search('!',DdessertL[i])
     if c!=None:
        if counterD>0 and counterD<7:
            cd=7-counterD
            for k in range(cd):
                dinnerDesserts.append('-')
            counterD=0
            rD=rD+1
     if counterD!=0:
      diff=len(DdessertfL[i])-len(DdessertfL[i].lstrip())
      for k in range(diff-1):
         dinnerDesserts.append('-')
         counterD=counterD+1
     if counterD==0 and rD>0:
      if lD[rD]>0:
       for j in range(lD[rD]):
        dinnerDesserts.append('-')
        counterD=counterD+1
     if counterD==0 and rD==0:
        diff=len(DdessertfL[i])-len(DdessertfL[i].lstrip())
        for k in range(diff):
         dinnerDesserts.append('-')
         counterD=counterD+1

     dinnerDesserts.append(DdessertfL[i].strip())
     counterD=counterD+1
     if counterD>=7:
        counterD=0
        rD=rD+1

 if len(dinnerDesserts)<len(dates):
    d=len(dates)-len(dinnerDesserts)
    for j in range(d):
        dinnerDesserts.append('-')
 
 #Get breakfast list
 brl=re.split('1η[\s]*[\n]*',breakfast)[1]
 brl=re.split('[0-9]*[0-9]/[0-9]*[0-9]/[0-9][0-9]',brl)
 brl = [re.sub('\n', '',s) for s in brl]
 brl = [re.sub('[0-9]η', '',s) for s in brl]
 for b in brl:
  b=b.strip()
 breakfast=brl[1:]
 if len(dinnerDesserts) == 32:
    dinnerDesserts = dinnerDesserts[:4] + dinnerDesserts[5:]

 print(len(dates),len(firstDishes),len(mainDishes1),len(mainDishes2),len(sideDishes),len(lunchDesserts),len(DfirstDishes),len(DmainDishes1),len(DmainDishes2),len(DsideDishes),len(dinnerDesserts),len(breakfast))
 
 today = datetime.date.today()

 n_dates=[]
 for d in dates:
    year = str(today.year)[-2:]
    p=re.split('[0-9]+\s*/\s*[0-9]+\s*/',d)
    s=d.replace(p[1],year)
    n_dates.append(s)

 #create json
 d = [ { 'day': x,'breakfast':l, 'lunch_first_dish': y, 'lunch_main_dish_1': z, 'lunch_main_dish_2':d,'lunch_side_dish':e,'lunch_dessert_1':'Φρούτο εποχής 2 επιλογές','lunch_dessert_2':f,'dinner_first_dish':g,'dinner_main_dish_1':h,'dinner_main_dish_2':i,'dinner_side_dish':j,'dinner_dessert_1':'Φρούτο εποχής 2 επιλογές','dinner_dessert_2':k } 
    for x,l, y, z,d,e,f,g,h,i,j,k in zip(n_dates,breakfast,firstDishes,mainDishes1,mainDishes2,sideDishes,lunchDesserts,DfirstDishes,DmainDishes1,DmainDishes2,DsideDishes,dinnerDesserts) ]
 filen = json.dumps(d, sort_keys=False, indent=4,ensure_ascii=False)

 month=re.split('/',dates[0])[1]
 month=re.split('/',month)[0]
 month_name=calendar.month_name[int(month)]
 fn=re.split('-',filename)[1]
 fn=month_name+'_'+fn

 with open(fn+'.json', 'w', encoding='utf-8') as f:
    f.write(filen)



#function to find and download pdf
def download_pdf():

 url = "https://www.upatras.gr/category/news/welfare/"

 # Requests URL and get response object
 response = requests.get(url)
 
 # Parse text obtained
 soup = BeautifulSoup(response.text, 'html.parser')
 elems=soup.find_all("a",{"class":"_self"})
 linklist=[]
 links=[]

 for el in elems:
  l=el.get("href")
  links.append(l)
 
 for link in links:
    r=re.search('programma-sitisis',link)
    if r is not None:
        linklist.append(link)

 new_url = linklist[0]
 
 x=re.search('minos',new_url)
 if x is not None:
    name=re.split('minos-',new_url)[1]
 elif 'maios' in new_url:
    year=re.split('sitisis-[A-Za-z-]*',new_url)[1]
    year=year.split('-')[0]
    name = 'May' + '-' + year
 elif 'oktovrios' in new_url:
    year=re.split('sitisis-[A-Za-z-]*',new_url)[1]
    year=year.split('-')[0]
    name = 'October' + '-' + year
 else:
    # Try to match date range format like "programma-sitisis-1-23-12-2025"
    date_range_match = re.search(r'sitisis-(\d+)-(\d+)-(\d+)-(\d+)', new_url)
    if date_range_match:
        # Format: sitisis-{start_day}-{end_day}-{month}-{year}
        month_num = int(date_range_match.group(3))
        year = date_range_match.group(4)
        name = calendar.month_name[month_num] + '-' + year
    else:
        name=re.split('sitisis-[A-Za-z-]*',new_url)[1]
        n=name.split('-')

        if len(n)==4:
            name=calendar.month_name[int(n[2])]
            name=name+'-'+n[3]
        else:
            name=calendar.month_name[int(n[1])]
            name=name+'-'+n[2]

 name=re.split('/',name)[0]

 # Requests URL and get response object
 response = requests.get(new_url)
 soup = BeautifulSoup(response.text, 'html.parser')


 l=soup.find_all("a")
 el=[]
 for e in l:
  el.append(e.get('href'))
 paragraphs = []
 for x in el:
    paragraphs.append(str(x))



 for i in range(len(el)):
    c=re.search('.pdf',paragraphs[i])
    a=re.search('ΠΡΟΓΡΑΜΜΑ-ΣΙΤΙΣΗΣ',paragraphs[i])
    if c is not None and a is not None:
        print(paragraphs[i],c)

        response = requests.get(el[i])
 
        pdf = open(name+".pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
 extract_from_pdf(name+".pdf",name)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    download_pdf()
    logger.info(f'Successful run.')