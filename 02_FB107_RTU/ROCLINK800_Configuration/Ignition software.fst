22Station Name        LOI
      CT FST 1, TMR1                   END                                                                             
      VALDIN A14, STATUS                                                                                               
      == 1                             IGNT                                                                            
      VALSFP 1, DATA2                                                                                                  
      == 1                             FLM_ST                                                                          
FLM_STVALAIN A9, EU                                                                                                    
      <  1400                          PL_STP                                                                          
      VALAIN A9, EU                                                                                                    
      >  1500                          PL_STR                                                                          
      GO END                                                                                                           
IGNT  DO DOU A12, STATUS               1                                                                               
      WT 30                                                                                                            
      GO FLM_ST                                                                                                        
ST_TM ST FST 1, TMR1                   1800                                                                            
      VAL0                                                                                                             
      SAVSFP 1, DATA1                                                                                                  
      GO END                                                                                                           
PL_STPDO DOU A12, STATUS               0                                                                               
      VAL0                                                                                                             
      SAVSFP 1, DATA2                                                                                                  
      VALSFP 1, DATA1                                                                                                  
      +  1                                                                                                             
      == 2                             ST_TM                                                                           
      GO END                                                                                                           
PL_STRVAL1                                                                                                             
      SAVSFP 1, DATA2                                                                                                  
      GO END                                                                                                           
END   END                                                                                                              
