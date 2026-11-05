flowchart TD

    A[main.py] -->|Ejecuta| B{¿Es día hábil?}
    
    B -- No --> C[Imprime "no es día hábil"\nTermina ejecución]
    B -- Sí --> D[FactoringXml.descargar_xml()]
    
    subgraph FactoringXml
        D --> E[Lee empresas desde credenciales.csv]
        E --> F[Abre navegador con Selenium]
        F --> G{Iterar por cada empresa}
        
        G -->|Login| H[Acceso portal SII]
        H -->|Falla login| I[envio_error():\n Captura pantalla y correo error]
        H -->|Éxito| J[Ingresar a Cesiones]
        
        J --> K{Consulta XMLs entre fechas}
        K -->|Error sitio (-999 o 500)| L[monitor_directory(driver)]
        L -->|Éxito descarga| M[Correo éxito + cerrar sesión]
        L -->|Falla en 10 intentos| I
        
        K -->|Sin error| M[Correo éxito + cerrar sesión]
        
        M --> G
        I --> G
        G --> N[Cierra navegador]
    end

    subgraph envio_correo
        I --> O[correo(mensaje, empresa, ruta_imagen)]
        M --> O
        O --> P[notificar():\n Construye HTML + POST a API correo]
    end
