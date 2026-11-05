import oracledb
import pandas as pd
import config_multi
from datetime import datetime
import os
from oracledb import makedsn

oracledb.init_oracle_client(lib_dir=r"C:\Scraping\PLSQL Python\instantclient\instantclient_23_9")
# Carpeta raíz donde se guardarán los resultados
CARPETA_BASE = r"\\columbia\cargas_masivas\TBK2"

# Consulta base (todas las empresas excepto AMA)
consulta_base = """
SELECT p.id_pago,
       oc.no_orden_compra,
       p.id_caja,
       c.nom_caja,
       p.fecha_apertura,
       p.id_servicio,
       p.fecha_pago,
       p.fecha_aplicacion,
       p.id_forma_pago,
       p.no_doc,
       trunc(d.fecha_deposito) as fecha_deposito,
       d.id_deposito,
       p.monto_pago,
       nvl(ab.monto,0) as abono_bomberos,
       (p.monto_pago + nvl(ab.monto, 0)) as total,
       (
        select max(cod_comercio)
          from dbo.relacion_caja_comercio rcc
         where rcc.id_caja = c.id_caja
       ) as cod_comercio
FROM dbo.relacion_pago_deposito rpd
JOIN dbo.deposito d 
    ON rpd.id_deposito = d.id_deposito
JOIN dbo.pago p 
    ON rpd.id_pago = p.id_pago
JOIN dbo.caja c 
    ON p.id_caja = c.id_caja
LEFT JOIN dbo.abono_bomberos ab
    ON ab.id_pago = p.id_pago
   AND ab.id_servicio = p.id_servicio
LEFT JOIN (
    select NO_ORDEN_COMPRA, ID_SERVICIO, FECHA_INTEGRACION  
    from sitioweb.orden_compra@db_sitios_web
    where estado = 'p' 
      and trunc(FECHA_INTEGRACION) >= sysdate - 7
    union
    select NO_ORDEN_COMPRA, ID_SERVICIO, FECHA_PROCESO as FECHA_INTEGRACION 
    from sitioweb.orden_portal_pago@db_sitios_web 
    where estado = 'p'
      and trunc(FECHA_PROCESO) >= sysdate - 7
) oc
    ON p.id_servicio = oc.id_servicio
   AND trunc(p.FECHA_PAGO) = trunc(oc.FECHA_INTEGRACION)
WHERE trunc(fecha_ingreso) = TO_DATE(:fecha_ingreso, 'DD/MM/YYYY')
  AND d.id_forma_pago = :id_forma_pago
ORDER BY p.fecha_pago ASC
"""

# Consulta especial para AMA
consulta_ama = """
SELECT p.id_pago,
       oc.no_orden_compra,
       p.id_caja,
       c.nom_caja,
       p.fecha_apertura,
       p.id_servicio,
       p.fecha_pago,
       p.fecha_aplicacion,
       p.id_forma_pago,
       p.no_doc,
       trunc(d.fecha_deposito) as fecha_deposito,
       d.id_deposito,
       p.monto_pago,
       nvl(ab.monto,0) as abono_bomberos,
       (p.monto_pago + nvl(ab.monto, 0)) as total,
       (
        select max(cod_comercio)
          from dbo.relacion_caja_comercio rcc
         where rcc.id_caja = c.id_caja
       ) as cod_comercio
FROM dbo.relacion_pago_deposito rpd
JOIN dbo.deposito d 
    ON rpd.id_deposito = d.id_deposito
JOIN dbo.pago p 
    ON rpd.id_pago = p.id_pago
JOIN dbo.caja c 
    ON p.id_caja = c.id_caja
LEFT JOIN dbo.abono_bomberos ab
    ON ab.id_pago = p.id_pago
   AND ab.id_servicio = p.id_servicio
LEFT JOIN (
    select NO_ORDEN_COMPRA, ID_SERVICIO, FECHA_INTEGRACION  
    from sitioweb.orden_compra@db_sitios_web
    where estado = 'p' 
      and trunc(FECHA_INTEGRACION) >= sysdate - 7
    union
    select NO_ORDEN_COMPRA, ID_SERVICIO, FECHA_PROCESO as FECHA_INTEGRACION 
    from sitioweb.orden_portal_pago@db_sitios_web 
    where estado = 'p'
      and trunc(FECHA_PROCESO) >= sysdate - 7
) oc
    ON p.id_servicio = oc.id_servicio
   AND trunc(p.FECHA_PAGO) = trunc(oc.FECHA_INTEGRACION)
WHERE trunc(fecha_ingreso) = TO_DATE(:fecha_ingreso, 'DD/MM/YYYY')
  AND d.id_forma_pago = :id_forma_pago
ORDER BY p.fecha_pago ASC
"""

# Fecha dinámica de hoy
hoy = datetime.today()
fecha_actual_str = hoy.strftime('%d/%m/%Y')

# Recorremos las empresas
for empresa, datos in config_multi.configuraciones.items():
    print(f"\n🔄 Procesando empresa: {empresa}")

    # Carpeta por empresa
    carpeta_empresa = os.path.join(CARPETA_BASE, empresa.upper())
    os.makedirs(carpeta_empresa, exist_ok=True)

    # Consulta según empresa
    sql = consulta_ama if empresa.upper() == "AMA" else consulta_base
    print(f"🔧 Consulta usada: {'AMA' if sql == consulta_ama else 'BASE'}")

    for forma, etiqueta in [(7, "debito"), (5, "credito")]:
       
        try:
            host = datos["host"]  # Define el host real aquí o en alguna configuración central
            port = datos["port"]
            service_name = datos["dsn"]
            dsn_completo = makedsn(host, port, service_name=service_name)

            connection = oracledb.connect(
                user=datos["username"],
                password=datos["password"],
                dsn=dsn_completo,
               
                
            )

            print(f"  🔍 Ejecutando consulta {etiqueta.upper()}...")

            df = pd.read_sql(
                sql,
                con=connection,
                params={
                    "id_forma_pago": forma,
                    "fecha_ingreso": fecha_actual_str
                }
            )

            connection.close()

            # Verificación especial para AMA
            if consulta_ama:
                columnas_verificadas = [col for col in df.columns if "PAGO" in col or "APLICACION" in col]
                print(f"\n🕒 Verificando columnas con hora en empresa AMA - {etiqueta.upper()}")
                print("Columnas disponibles:", columnas_verificadas)
                print(df[columnas_verificadas].dtypes)
                print(df[columnas_verificadas].head())

            if not df.empty:
                fecha_deposito = df['FECHA_DEPOSITO'].max()

                if pd.notnull(fecha_deposito):
                    fecha_str = fecha_deposito.strftime("%d%m%Y")
                else:
                    fecha_str = "sin_fecha"

                # Subcarpeta por fecha
                subcarpeta_fecha = os.path.join(carpeta_empresa, fecha_str)
                os.makedirs(subcarpeta_fecha, exist_ok=True)

                # Guardar archivo
                nombre_archivo = f"{etiqueta.lower()}_{empresa.lower()}_{fecha_str}.xlsx"
                ruta_archivo = os.path.join(subcarpeta_fecha, nombre_archivo)

                try:
                    df.to_excel(ruta_archivo, index=False)
                    print(f"    ✅ Archivo guardado: {ruta_archivo}")
                except PermissionError:
                    print(f"    ⚠️  No se pudo guardar (archivo en uso): {ruta_archivo}")
                except Exception as e:
                    print(f"    ⚠️  Error al guardar archivo {ruta_archivo}: {str(e)}")
            else:
                print(f"  ⚠️  Sin datos para {empresa} - {etiqueta.upper()}")

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"  ❌ Error en {empresa} ({etiqueta}): {error.message}")
