import os
configuraciones = {
"SGC_ADA":{
    "host"      : "192.172.1.11",
    "username"  : "interno"    , 
    "password"  : os.getenv("ORACLE_PASSWORD_SGC_ADA"),     
    "dsn"       : "SGC01"    ,
    "port"      : 1681,
    "encoding"  :"UTF-8",
   
        
    },
     "SGC_ATA": {
        "host"      :  "192.172.1.25",
        "username"  : "interno",
        "password"  : os.getenv("ORACLE_PASSWORD_SGC_ATA"),
        "dsn"       : "SGC03",
        "port"      : 1681,
        "encoding"  : "UTF-8",
        
    }, 
    "SGC_ARA": {
        "host"      : "192.172.1.17",
        "username"  : "interno",
        "password"  : os.getenv("ORACLE_PASSWORD_SGC_ARA"),
        "dsn"       : "SGC09",
        "port"      : 1681,
        "encoding"  : "UTF-8",
     
   },
     "SGC_AXA": {
         "host"      : "192.172.1.16",
        "username"  : "interno",
        "password"  : os.getenv("ORACLE_PASSWORD_SGC_AXA"),
        "dsn"       : "SGC10",
        "port"      : 1681,
        "encoding"  : "UTF-8",
        
    },
     "SGC_AMA": {
         "host"      : "192.172.1.131",
        "username"  : "interno",
        "password"  : os.getenv("ORACLE_PASSWORD_SGC_AMA"),
        "dsn"       : "SGC12",
        "port"      : 1681,
        "encoding"  : "UTF-8",
        
      
    },




}