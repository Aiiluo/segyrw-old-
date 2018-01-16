# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 21:28:04 2018

@author: Judyan
"""

import struct
import read_segy_header
import numpy as np

class segy3d(read_segy_header.segyheader):
    
    def __init___(self):
        read_segy_header.segyheader.__init__(self)
        self.init_binary_header()
#        (self.inline_start,self.xline_start,self.X_min,self.Y_min) = self.read_control_file(1)
#        (self.inline_end,self.xline_end,self.X_max,self.Y_max) = self.read_last_trace_header()
#        self.inline_lens = self.inline_end - self.inline_start + 1
#        self.xline_lens = self.xline_end - self.xline_start + 1
#        self.trace_count = self.inline_lens * self.xline_lens


        

    def segy_information(self):
        self.read_binary_header()
        
        (self.inline_start,self.xline_start,self.X_min,self.Y_min) = self.read_control_file(1)
        (self.inline_end,self.xline_end,self.X_max,self.Y_max) = self.read_last_trace_header()
        self.inline_lens = self.inline_end - self.inline_start + 1
        self.xline_lens = self.xline_end - self.xline_start + 1
        self.trace_count = self.inline_lens * self.xline_lens
        print("=================== Segy Information =======================")
        print("inline:",self.inline_start," to ",self.inline_end)
        print("xline:",self.xline_start," to ",self.xline_end)
        print("coordinate X:",self.X_min," to ",self.X_max)
        print("coordinate Y:",self.Y_min," to ",self.Y_max)
        print("inline lens:",self.inline_lens)
        print("xline lens:",self.xline_lens)
        
    
    
    def read_3dSegy_data(self,inline,xline):
        
        
        if self.data_fmt == 1:
            self.read_ibmfloat_data(inline,xline)
        elif self.data_fmt == 2:
            self.read_int32_data(inline,xline)
        elif self.data_fmt == 3:
            self.read_int16_data(inline,xline)
        elif self.data_fmt == 5:
            self.read_IEEEfloat_data(inline,xline)
        elif self.data_fmt == 8:
            self.read_int8_data(inline,xline)
        else:
            return "This format is no use now."
        
    def read_int8_data(self,inline,xline):
        
        self.init_binary_header()
        (self.inline_start,self.xline_start,self.X_min,self.Y_min) = self.read_control_file(1)
        (self.inline_end,self.xline_end,self.X_max,self.Y_max) = self.read_last_trace_header()
        self.inline_lens = self.inline_end - self.inline_start + 1
        self.xline_lens = self.xline_end - self.xline_start + 1
        self.trace_count = self.inline_lens * self.xline_lens
        
                
        trace_position = (inline-self.inline_start)*self.xline_lens + (xline-self.xline_start)
        start_number = self.text_header_lens+self.bin_header_lens
        data_lens = self.number_of_sample * self.sample_fmt
        trace_lens = data_lens + self.trace_header_lens
        start = start_number+trace_position*trace_lens+self.trace_header_lens
        unpack_fmt = '>' + str(self.number_of_sample) + 'b'
        
        Int8 = np.zeros(self.number_of_sample,dtype=np.int8)
        with open(self.segy_file,'rb') as in_file:
            in_file.seek(start)
            data = in_file.read(data_lens)
            Int8 = np.asarray(struct.unpack(unpack_fmt,data))
            
        return Int8
    
    def IBM2float(self,ibm_float):
        p24 = float(pow(2,24))
        if ibm_float == 0:
            return 0.0
        sign = ibm_float >> 31 & 0x01
        exponent = ibm_float >> 24 & 0x7f 
        mantissa = (ibm_float & 0x00ffffff)/p24 
        return (1-2*sign)*(mantissa)*pow(16,exponent-64)
    
    def read_ibmfloat_data(self,inline,xline):
    
        self.init_binary_header()
        (self.inline_start,self.xline_start,self.X_min,self.Y_min) = self.read_control_file(1)
        (self.inline_end,self.xline_end,self.X_max,self.Y_max) = self.read_last_trace_header()
        self.inline_lens = self.inline_end - self.inline_start + 1
        self.xline_lens = self.xline_end - self.xline_start + 1
        self.trace_count = self.inline_lens * self.xline_lens
        
                
        trace_position = (inline-self.inline_start)*self.xline_lens + (xline-self.xline_start)
        start_number = self.text_header_lens+self.bin_header_lens
        data_lens = self.number_of_sample * self.sample_fmt
        trace_lens = data_lens + self.trace_header_lens
        start = start_number+trace_position*trace_lens+self.trace_header_lens
        unpack_fmt = '>' + str(self.number_of_sample) + 'i'
        IBM_float = [0] * self.number_of_sample       
#        IBM_float = np.zeros(self.number_of_sample,dtype=np.int32)
        PC_float = np.zeros(self.number_of_sample,dtype=np.float32)
        with open(self.segy_file,'rb') as in_file:
            in_file.seek(start)
            data = in_file.read(data_lens)
#            IBM_float = np.asarray(struct.unpack(unpack_fmt,data))
            IBM_float = list(struct.unpack(unpack_fmt,data))
        
        for i in range(0,self.number_of_sample):
            PC_float[i] = self.IBM2float(IBM_float[i])
            
        return PC_float

        
   
    
            
        