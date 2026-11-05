import cx_Oracle
import config 
import pandas as pd


connection = None


def consultar_saldos():
    dia=input("Ingresar día: ")
    try:
        connection = cx_Oracle.connect(
            config.username,
            config.password,
            config.dsn,
            encoding=config.encoding)

        cursor=connection.cursor()
        print("*******************BANCO DE CHILE*********************************")
        sqlSelect="SELECT fecha, CASE WHEN rutempresa = '76.038.659-6' THEN 'AN' WHEN rutempresa = '96.703.230-1' THEN 'AXA' WHEN rutempresa = '76.850.128-9' THEN 'ATA' WHEN rutempresa = '76.215.637-7' THEN 'ARA' WHEN rutempresa = '76.215.628-8' THEN 'AMA' WHEN rutempresa = '76.215.634-2' THEN 'ADA' end empresa, rutempresa, SUM(abonos), SUM(cargos) "\
                    "FROM integracion.depositos_bancochile WHERE TO_DATE(fecha, 'dd/mm/yyyy') >= trunc(sysdate)-"+dia+" GROUP BY fecha,rutempresa ORDER BY TO_DATE(fecha, 'dd/mm/yyyy'), rutempresa"
        cursor.execute(sqlSelect)
        depositos_chile = cursor.fetchall()
        banco_chile=[]
        for row in depositos_chile:
            banco_chile.append(row)
        df1=pd.DataFrame(banco_chile, columns=['FECHA','EMPRESA','RUTEMPRESA','SUM(ABONOS)','SUM(CARGOS)'])
        print(df1)
        print("*******************FIN********************************************")

        print("\n")    

        print("*******************BANCO ESTADO*********************************")
        sqlSelect1="SELECT fecha,alias,sum(depositos_abonos),sum(cheques_cargos) "\
                    "FROM integracion.depositos_bancoestado WHERE TO_DATE(fecha, 'dd/mm/yyyy') >= trunc(sysdate)-"+dia+" GROUP BY fecha, alias ORDER BY TO_DATE(fecha, 'dd/mm/yyyy'), alias"
        cursor.execute(sqlSelect1)
        depositos_estado = cursor.fetchall()
        banco_estado=[]
        for estado in depositos_estado:
            banco_estado.append(estado)
        df2=pd.DataFrame(banco_estado, columns=['FECHA','ALIAS','SUM(depositos_abonos)','SUM(cheques_cargos)'])
        print(df2)
        print("*******************FIN********************************************")

        print("\n")    

        print("*******************BANCO BCI*********************************")
        sqlSelect2="SELECT fecha_contable,empresa,sum(abono),sum(cargo)"\
                    "from integracion.depositos_bci where to_date(fecha_contable, 'dd/mm/yyyy') >= trunc(sysdate)-"+dia+" group by fecha_contable,empresa order by to_date(fecha_contable, 'dd/mm/yyyy'), empresa"
        cursor.execute(sqlSelect2)
        depositos_bci = cursor.fetchall()
        banco_bci=[]
        for bci in depositos_bci:
            banco_bci.append(bci)
        df3=pd.DataFrame(banco_bci, columns=['FECHA_CONTABLE','EMPRESA','SUM(ABONO)','SUM(CARGO)'])
        print(df3)
        print("*******************FIN********************************************")

        print("\n")    

        print("*******************BANCO ITAU*********************************")
        sqlSelect3=f"SELECT (substr(fecha,1,instr(fecha,' ')-1)) fecha,empresa,sum(depositos_o_abonos)"\
                    "from integracion.depositos_itau where to_date(substr(fecha,1,instr(fecha,' ')-1),'yyyy-mm-dd') >= trunc(sysdate)-"+dia+" group by (substr(fecha,1,instr(fecha,' ')-1)) , empresa order by to_date(substr(fecha,1,instr(fecha,' ')-1),'yyyy-mm-dd') asc"
        cursor.execute(sqlSelect3)
        depositos_itau = cursor.fetchall()
        banco_itau=[]
        for itau in depositos_itau:
            banco_itau.append(itau)
        df4=pd.DataFrame(banco_itau, columns=['FECHA','EMPRESA','SUM(DEPOSITOS_O_ABONOS)'])
        print(df4)
        print("*******************FIN********************************************")

        print("\n")    

        print("*******************BANCO SANTANDER*********************************")
        sqlSelect4="SELECT fecha,case when rut_empresa = '96.703.230-1' then 'AXA' when rut_empresa = '76.850.128-9' then 'ATA' when rut_empresa = '76.215.637-7' then 'ARA' when rut_empresa = '76.215.628-8' then 'AMA' when rut_empresa = '76.215.634-2' then 'ADA' else rut_empresa end empresa, sum(monto), cargo_abono FROM integracion.depositos_santander where to_date(fecha, 'dd/mm/yyyy') >= trunc(sysdate)-"+dia+" group by fecha, rut_empresa, cargo_abono order by to_date(fecha, 'dd/mm/yyyy'), empresa asc"
        cursor.execute(sqlSelect4)
        depositos_santander = cursor.fetchall()
        banco_santander=[]
        for santander in depositos_santander:
            banco_santander.append(santander)
        df5=pd.DataFrame(banco_santander, columns=['FECHA','EMPRESA','SUM(MONTO)','CARGO_ABONO'])
        print(df5)
        print("*******************FIN********************************************")

        opcion=input("Para volver a consultar, presione la tecla 's'. Para salir presione cualquier tecla... ") 

        if opcion=='s':
            consultar_saldos()


    except Exception as error:
        print(error)


           
    connection.close()

consultar_saldos()


