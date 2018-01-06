# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 22:09:17 2018
@author: Aiiluo

This Modul is made for reading the EBCDIC header of seismic segy data,
and translate the EBCDIC code to ASCII code.
"""


def ebc2asc(ebc_input): #定义ECBDIC转ASCII的字典
    dict = [
            'NUL','SOH','STX','ETX','SEL','HT','RNL','DEL','GE','SPS','RPT','VT','FF','CR','SO','SI',
            'DLE','DC','DC','DC','RE','NL','BS','POC','CAN','EM','UBS','CU','IFS','IGS','IRS','IUSIT',
            'DS','SOS','FS','WUS','BYP','LF','ETB','ESC','SA','SFE','SMS','CSP','MFA','ENQ','ACK','BEL',
            ' ',' ','SYN','IR','PP','TRN','NBS','EOT','SBS','IT','RFF','CU','DC','NAK',' ','SUB',
            ' ','RSP',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','<','(','+','|',
            '&',' ',' ',' ',' ',' ',' ',' ',' ',' ','!','$','*',')',';','&not',
            '-','/',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','%','_','>','?',
            ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',':','#','@',' ','=','"',
            ' ','a','b','c','d','e','f','g','h','i',' ',' ',' ',' ',' ','+_',
            ' ','j','k','l','m','n','o','p','q','r',' ',' ',' ',' ',' ',' ',
            ' ','~','s','t','u','v','w','x','y','z',' ',' ',' ',' ',' ',' ',
            '^',' ',' ',' ',' ',' ',' ',' ',' ',' ','[',']',' ',' ',' ',' ',
            '{','A','B','C','D','E','F','G','H','I','SHY',' ',' ',' ',' ',' ',
            '}','J','K','L','M','N','O','P','Q','R',' ',' ',' ',' ',' ',' ',
            ' ',' ','S','T','U','V','W','X','Y','Z',' ',' ',' ',' ',' ',' ',
            '0','1','2','3','4','5','6','7','8','9',' ',' ',' ',' ',' ','EO',
            ]
    int_ebc = int(ebc_input)
    asc_output = dict[int_ebc]
    return asc_output

def Read_EBCDIC(segy_data): #读取文本头
    print("================ EBCDIC Header=================\n")
    asc = list(range(3200))
    asc_line = list(range(3240))
    m = 0
    with open(segy_data,'rb') as in_file:
        data = in_file.readline()    
        for i in range(0,3200):
            asc[i] = ebc2asc(data[i])
            
    for j in range(0,3200,80):        
        for k in range(0,80):
            asc_line[j+k+m] = asc[j+k]
        asc_line[j+k+m+1] = '\n'
        m = m + 1
    asc_str = ''.join(asc_line)  
      
    return asc_str

    
