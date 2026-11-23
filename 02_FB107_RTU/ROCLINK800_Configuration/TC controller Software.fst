22Station Name        !LOI
      VAL350                                                                                                           
      SAVSFP 3, DATA1                                                                                                  
      VALSFP 3, DATA1                                                                                                  
      -  20                                                                                                            
      SAVSFP 3, DATA2                                                                                                  
      VALAIN A10, EU                                                                                                   
      >  SFP 3, DATA1                  CLS_VL                                                                          
      VALAIN A10, EU                                                                                                   
      <  SFP 3, DATA2                  OPN_VL                                                                          
CLS_VLDO DOU A11, STATUS               0                                                                               
      GO END                                                                                                           
OPN_VLDO DOU A11, STATUS               1                                                                               
END   END                                                                                                              
