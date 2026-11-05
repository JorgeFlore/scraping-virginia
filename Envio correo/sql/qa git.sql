CREATE OR REPLACE PACKAGE SITIOWEB_2.METODOS_SGC20_CONVENIO
AS
    TYPE t_cursor IS REF CURSOR;

    PROCEDURE solicitud_crear_convenio (p_id_empresa             NUMBER,
                                        p_id_servicio            NUMBER,
                                        p_canal                  NUMBER,
                                        p_crear_convenio     OUT NUMBER,
                                        p_id_tipo_convenio   OUT NUMBER,
                                        p_pedir_pie          OUT NUMBER,
                                        p_total_deuda_conv   OUT NUMBER,
                                        p_pie_minimo         OUT NUMBER,
                                        p_pie_maximo         OUT NUMBER,
                                        p_deuda_vencida      OUT NUMBER,
                                        p_deuda_no_vencida   OUT NUMBER,
                                        p_antiguedad         OUT NUMBER,
                                        p_deuda_convenida    OUT NUMBER,
                                        p_deuda_cobranza     OUT NUMBER,
                                        p_mensaje            OUT VARCHAR2,
                                        p_is_ok              OUT NUMBER);

    PROCEDURE valida_pie_convenio (p_id_empresa            NUMBER,
                                   p_pie_minimo_us         NUMBER,
                                   p_pie_minimo_df         NUMBER,
                                   p_pie_maximo_df         NUMBER,
                                   p_tipo_convenio         NUMBER,
                                   p_deuda_total           NUMBER,
                                   p_opcion_monto_1    OUT NUMBER,
                                   p_opcion_cuotas_1   OUT NUMBER,
                                   p_opcion_monto_2    OUT NUMBER,
                                   p_opcion_cuotas_2   OUT NUMBER,
                                   p_opcion_monto_3    OUT NUMBER,
                                   p_opcion_cuotas_3   OUT NUMBER,
                                   p_opcion_monto_4    OUT NUMBER,
                                   p_opcion_cuotas_4   OUT NUMBER,
                                   p_opcion_monto_5    OUT NUMBER,
                                   p_opcion_cuotas_5   OUT NUMBER,
                                   p_opcion_monto_6    OUT NUMBER,
                                   p_opcion_cuotas_6   OUT NUMBER,
                                   p_no_opciones       OUT NUMBER,
                                   p_mensaje           OUT VARCHAR2,
                                   p_is_ok             OUT NUMBER);

    PROCEDURE crea_convenio_web (p_id_empresa              NUMBER,
                                 p_id_servicio             NUMBER,
                                 p_id_tipo_convenio        NUMBER,
                                 p_monto_pie               NUMBER,
                                 p_monto_cuota             NUMBER,
                                 p_no_cuotas               NUMBER,
                                 p_total_deuda_conv        NUMBER,
                                 p_deuda_vencida           NUMBER,
                                 p_deuda_no_vencida        NUMBER,
                                 p_antiguedad              NUMBER,
                                 p_deuda_convenida         NUMBER,
                                 p_numero_serie_ci         VARCHAR2,
                                 p_fecha_vencimiento       DATE,
                                 p_canal                   NUMBER,
                                 p_id_convenio         OUT NUMBER,
                                 p_recordset           OUT SYS_REFCURSOR,
                                 p_mensaje             OUT VARCHAR2,
                                 p_is_ok               OUT NUMBER);

    PROCEDURE eliminar_convenio_web (p_id_empresa        NUMBER,
                                     p_id_convenio       NUMBER,
                                     p_canal             NUMBER,
                                     p_mensaje       OUT VARCHAR2,
                                     p_is_ok         OUT NUMBER);

    PROCEDURE consulta_convenio_matico (p_id_empresa              NUMBER,
                                        p_id_servicio             NUMBER,
                                        p_fecha_convenio      OUT VARCHAR2,
                                        p_id_convenio         OUT NUMBER,
                                        p_monto_pie           OUT NUMBER,
                                        p_monto_convenido     OUT NUMBER,
                                        p_n_cuotas_emitidas   OUT NUMBER,
                                        p_no_cuotas           OUT NUMBER,
                                        p_estado              OUT VARCHAR2,
                                        p_mensaje             OUT VARCHAR2,
                                        p_is_ok               OUT NUMBER);

    PROCEDURE elimina_convenio_matico (p_id_empresa        NUMBER,
                                       p_id_convenio       NUMBER,
                                       p_mensaje       OUT VARCHAR2,
                                       p_is_ok         OUT NUMBER);

    PROCEDURE consulta_tipo_convenio (p_id_empresa        NUMBER,
                                      p_id_servicio       NUMBER,
                                      cur             OUT T_CURSOR,
                                      p_is_ok         OUT NUMBER,
                                      p_mensaje       OUT VARCHAR2);

    PROCEDURE solicitud_crear_convenio_cyr (
        p_id_empresa                NUMBER,
        p_id_servicio               NUMBER,
        p_canal                     NUMBER,
        p_id_tipo_convenio_in       NUMBER,
        p_crear_convenio        OUT NUMBER,
        p_id_tipo_convenio      OUT NUMBER,
        p_pedir_pie             OUT NUMBER,
        p_total_deuda_conv      OUT NUMBER,
        p_pie_minimo            OUT NUMBER,
        p_pie_maximo            OUT NUMBER,
        p_deuda_vencida         OUT NUMBER,
        p_deuda_no_vencida      OUT NUMBER,
        p_antiguedad            OUT NUMBER,
        p_deuda_convenida       OUT NUMBER,
        p_deuda_cobranza        OUT NUMBER,
        p_mensaje               OUT VARCHAR2,
        p_is_ok                 OUT NUMBER);

    PROCEDURE crea_convenio_web_CYR (p_id_empresa              NUMBER,
                                     p_id_servicio             NUMBER,
                                     p_id_tipo_convenio        NUMBER,
                                     p_monto_pie               NUMBER,
                                     p_monto_cuota             NUMBER,
                                     p_no_cuotas               NUMBER,
                                     p_total_deuda_conv        NUMBER,
                                     p_deuda_vencida           NUMBER,
                                     p_deuda_no_vencida        NUMBER,
                                     p_antiguedad              NUMBER,
                                     p_deuda_convenida         NUMBER,
                                     p_numero_serie_ci         VARCHAR2,
                                     p_fecha_vencimiento       DATE,
                                     p_canal                   NUMBER,
                                     p_nombre_apellido         VARCHAR2,
                                     p_rut                     NUMBER,
                                     p_telefono                NUMBER,
                                     p_id_convenio         OUT NUMBER,
                                     p_recordset           OUT SYS_REFCURSOR,
                                     p_mensaje             OUT VARCHAR2,
                                     p_is_ok               OUT NUMBER);

    /* Modificación [IJM] 17/10/2022  - Sarche Service SpA
    Mejoras Convenio Sitios WEB
 */

    PROCEDURE consulta_tipo_convenio_texto (p_id_empresa        NUMBER,
                                            p_id_servicio       NUMBER,
                                            cur             OUT T_CURSOR,
                                            p_is_ok         OUT NUMBER,
                                            p_mensaje       OUT VARCHAR2);
END;
/


CREATE OR REPLACE PACKAGE BODY SITIOWEB_2.METODOS_SGC20_CONVENIO
AS
    PROCEDURE solicitud_crear_convenio (p_id_empresa             NUMBER,
                                        p_id_servicio            NUMBER,
                                        p_canal                  NUMBER,
                                        p_crear_convenio     OUT NUMBER,
                                        p_id_tipo_convenio   OUT NUMBER,
                                        p_pedir_pie          OUT NUMBER,
                                        p_total_deuda_conv   OUT NUMBER,
                                        p_pie_minimo         OUT NUMBER,
                                        p_pie_maximo         OUT NUMBER,
                                        p_deuda_vencida      OUT NUMBER,
                                        p_deuda_no_vencida   OUT NUMBER,
                                        p_antiguedad         OUT NUMBER,
                                        p_deuda_convenida    OUT NUMBER,
                                        p_deuda_cobranza     OUT NUMBER,
                                        p_mensaje            OUT VARCHAR2,
                                        p_is_ok              OUT NUMBER)
    IS
        p_cont          NUMBER := 0;
        v_canal         NUMBER;
        p_mensaje_log   VARCHAR2 (4000);
    BEGIN
        IF p_id_empresa = 1
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC01
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
                p_mensaje_log := p_mensaje || ' (Cód. 001)';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio@link_sitioweb_sgc01 (
                    p_id_servicio,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        ELSIF p_id_empresa = 9
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC09
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
                p_mensaje_log := p_mensaje || ' (Cód. 001)';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio@link_sitioweb_sgc09 (
                    p_id_servicio,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        ELSIF p_id_empresa = 10
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC10
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
                p_mensaje_log := p_mensaje || ' (Cód. 001)';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio@LINK_SITIOWEB_SGC10 (
                    p_id_servicio,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        ELSIF p_id_empresa = 3
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC03
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
                p_mensaje_log := p_mensaje || ' (Cód. 001)';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio@link_sitioweb_sgc03 (
                    p_id_servicio,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        ELSIF p_id_empresa = 12
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC12
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
                p_mensaje_log := p_mensaje || ' (Cód. 001)';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio@link_sitioweb_sgc12 (
                    p_id_servicio,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        END IF;


        IF p_is_ok = 0
        THEN
            IF p_canal IS NULL OR p_canal = 0
            THEN
                v_canal := 17;                                  -- app  mobile
            ELSE
                v_canal := p_canal;
            END IF;


            INSERT INTO log_usua_metodo_canal (usua_num_cliente,
                                               usua_empresa,
                                               id_metodo,
                                               canal_ingreso,
                                               fecha)
                     VALUES (
                         UPPER (
                                TRIM (p_id_servicio)
                             || '-'
                             || dv_mod11 (p_id_servicio)),
                         p_id_empresa,
                         6,                         --solicitud crea convenio,
                         v_canal,
                         SYSDATE);
        END IF;

        IF p_crear_convenio IS NULL
        THEN
            -- Respaldo mensaje de error para log
            p_mensaje_log := p_mensaje || ' (Cód. 002)';
            p_crear_convenio := 0;
            -- Mensaje de error genérico para el cliente
            p_mensaje :=
                'Estimado cliente: Las condiciones de su servicio no permiten generar un convenio a través del sitio web. Por favor, dirígete a tu Centro de Atención de Clientes más cercano.';
            p_is_ok := 1;
        END IF;

        IF p_mensaje_log IS NULL
        THEN
            p_mensaje_log := p_mensaje || ' (Cód. 003)';
        END IF;

        INSERT INTO log_solicitud_crear_convenio (p_id_empresa,
                                                  p_id_servicio,
                                                  p_canal,
                                                  p_crear_convenio,
                                                  p_id_tipo_convenio,
                                                  p_pedir_pie,
                                                  p_total_deuda_conv,
                                                  p_pie_minimo,
                                                  p_pie_maximo,
                                                  p_deuda_vencida,
                                                  p_deuda_no_vencida,
                                                  p_antiguedad,
                                                  p_deuda_convenida,
                                                  p_deuda_cobranza,
                                                  p_mensaje,
                                                  p_is_ok)
             VALUES (p_id_empresa,
                     p_id_servicio,
                     p_canal,
                     p_crear_convenio,
                     p_id_tipo_convenio,
                     p_pedir_pie,
                     p_total_deuda_conv,
                     p_pie_minimo,
                     p_pie_maximo,
                     p_deuda_vencida,
                     p_deuda_no_vencida,
                     p_antiguedad,
                     p_deuda_convenida,
                     p_deuda_cobranza,
                     p_mensaje_log,
                     p_is_ok);

        COMMIT;
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;

    PROCEDURE valida_pie_convenio (p_id_empresa            NUMBER,
                                   p_pie_minimo_us         NUMBER,
                                   p_pie_minimo_df         NUMBER,
                                   p_pie_maximo_df         NUMBER,
                                   p_tipo_convenio         NUMBER,
                                   p_deuda_total           NUMBER,
                                   p_opcion_monto_1    OUT NUMBER,
                                   p_opcion_cuotas_1   OUT NUMBER,
                                   p_opcion_monto_2    OUT NUMBER,
                                   p_opcion_cuotas_2   OUT NUMBER,
                                   p_opcion_monto_3    OUT NUMBER,
                                   p_opcion_cuotas_3   OUT NUMBER,
                                   p_opcion_monto_4    OUT NUMBER,
                                   p_opcion_cuotas_4   OUT NUMBER,
                                   p_opcion_monto_5    OUT NUMBER,
                                   p_opcion_cuotas_5   OUT NUMBER,
                                   p_opcion_monto_6    OUT NUMBER,
                                   p_opcion_cuotas_6   OUT NUMBER,
                                   p_no_opciones       OUT NUMBER,
                                   p_mensaje           OUT VARCHAR2,
                                   p_is_ok             OUT NUMBER)
    IS
    BEGIN
        IF p_id_empresa = 1
        THEN
            pkg_validaciones_convenio_web.valida_pie_convenio@link_sitioweb_sgc01 (
                p_pie_minimo_us,
                p_pie_minimo_df,
                p_pie_maximo_df,
                p_tipo_convenio,
                p_deuda_total,
                p_opcion_cuotas_1,
                p_opcion_monto_1,
                p_opcion_cuotas_2,
                p_opcion_monto_2,
                p_opcion_cuotas_3,
                p_opcion_monto_3,
                p_opcion_cuotas_4,
                p_opcion_monto_4,
                p_opcion_cuotas_5,
                p_opcion_monto_5,
                p_opcion_cuotas_6,
                p_opcion_monto_6,
                p_no_opciones,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 9
        THEN
            pkg_validaciones_convenio_web.valida_pie_convenio@link_sitioweb_sgc09 (
                p_pie_minimo_us,
                p_pie_minimo_df,
                p_pie_maximo_df,
                p_tipo_convenio,
                p_deuda_total,
                p_opcion_cuotas_1,
                p_opcion_monto_1,
                p_opcion_cuotas_2,
                p_opcion_monto_2,
                p_opcion_cuotas_3,
                p_opcion_monto_3,
                p_opcion_cuotas_4,
                p_opcion_monto_4,
                p_opcion_cuotas_5,
                p_opcion_monto_5,
                p_opcion_cuotas_6,
                p_opcion_monto_6,
                p_no_opciones,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 10
        THEN
            pkg_validaciones_convenio_web.valida_pie_convenio@LINK_SITIOWEB_SGC10 (
                p_pie_minimo_us,
                p_pie_minimo_df,
                p_pie_maximo_df,
                p_tipo_convenio,
                p_deuda_total,
                p_opcion_cuotas_1,
                p_opcion_monto_1,
                p_opcion_cuotas_2,
                p_opcion_monto_2,
                p_opcion_cuotas_3,
                p_opcion_monto_3,
                p_opcion_cuotas_4,
                p_opcion_monto_4,
                p_opcion_cuotas_5,
                p_opcion_monto_5,
                p_opcion_cuotas_6,
                p_opcion_monto_6,
                p_no_opciones,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 3
        THEN
            pkg_validaciones_convenio_web.valida_pie_convenio@link_sitioweb_sgc03 (
                p_pie_minimo_us,
                p_pie_minimo_df,
                p_pie_maximo_df,
                p_tipo_convenio,
                p_deuda_total,
                p_opcion_cuotas_1,
                p_opcion_monto_1,
                p_opcion_cuotas_2,
                p_opcion_monto_2,
                p_opcion_cuotas_3,
                p_opcion_monto_3,
                p_opcion_cuotas_4,
                p_opcion_monto_4,
                p_opcion_cuotas_5,
                p_opcion_monto_5,
                p_opcion_cuotas_6,
                p_opcion_monto_6,
                p_no_opciones,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 12
        THEN
            pkg_validaciones_convenio_web.valida_pie_convenio@link_sitioweb_sgc12 (
                p_pie_minimo_us,
                p_pie_minimo_df,
                p_pie_maximo_df,
                p_tipo_convenio,
                p_deuda_total,
                p_opcion_cuotas_1,
                p_opcion_monto_1,
                p_opcion_cuotas_2,
                p_opcion_monto_2,
                p_opcion_cuotas_3,
                p_opcion_monto_3,
                p_opcion_cuotas_4,
                p_opcion_monto_4,
                p_opcion_cuotas_5,
                p_opcion_monto_5,
                p_opcion_cuotas_6,
                p_opcion_monto_6,
                p_no_opciones,
                p_mensaje,
                p_is_ok);
        END IF;
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;


    PROCEDURE crea_convenio_web (p_id_empresa              NUMBER,
                                 p_id_servicio             NUMBER,
                                 p_id_tipo_convenio        NUMBER,
                                 p_monto_pie               NUMBER,
                                 p_monto_cuota             NUMBER,
                                 p_no_cuotas               NUMBER,
                                 p_total_deuda_conv        NUMBER,
                                 p_deuda_vencida           NUMBER,
                                 p_deuda_no_vencida        NUMBER,
                                 p_antiguedad              NUMBER,
                                 p_deuda_convenida         NUMBER,
                                 p_numero_serie_ci         VARCHAR2,
                                 p_fecha_vencimiento       DATE,
                                 p_canal                   NUMBER,
                                 p_id_convenio         OUT NUMBER,
                                 p_recordset           OUT SYS_REFCURSOR,
                                 p_mensaje             OUT VARCHAR2,
                                 p_is_ok               OUT NUMBER)
    IS
        v_canal   NUMBER;
    BEGIN
        IF p_id_empresa = 1
        THEN
            pkg_validaciones_convenio_web.crear_convenio_web@link_sitioweb_sgc01 (
                p_id_servicio,
                p_id_tipo_convenio,
                p_monto_pie,
                p_monto_cuota,
                p_no_cuotas,
                p_total_deuda_conv,
                p_deuda_vencida,
                p_deuda_no_vencida,
                p_antiguedad,
                p_deuda_convenida,
                NULL,                                     --p_estado_cobranza,
                p_numero_serie_ci,
                p_fecha_vencimiento,
                p_canal,
                p_id_convenio,
                p_mensaje,
                p_is_ok);


            OPEN p_recordset FOR
                SELECT *
                  FROM comprobante_convenio_web@link_sitioweb_sgc01
                 WHERE id_convenio = p_id_convenio;
        ELSIF p_id_empresa = 9
        THEN
            pkg_validaciones_convenio_web.crear_convenio_web@link_sitioweb_sgc09 (
                p_id_servicio,
                p_id_tipo_convenio,
                p_monto_pie,
                p_monto_cuota,
                p_no_cuotas,
                p_total_deuda_conv,
                p_deuda_vencida,
                p_deuda_no_vencida,
                p_antiguedad,
                p_deuda_convenida,
                NULL,                                     --p_estado_cobranza,
                p_numero_serie_ci,
                p_fecha_vencimiento,
                p_canal,
                p_id_convenio,
                p_mensaje,
                p_is_ok);


            OPEN p_recordset FOR
                SELECT *
                  FROM comprobante_convenio_web@link_sitioweb_sgc09
                 WHERE id_convenio = p_id_convenio;
        ELSIF p_id_empresa = 10
        THEN
            pkg_validaciones_convenio_web.crear_convenio_web@LINK_SITIOWEB_SGC10 (
                p_id_servicio,
                p_id_tipo_convenio,
                p_monto_pie,
                p_monto_cuota,
                p_no_cuotas,
                p_total_deuda_conv,
                p_deuda_vencida,
                p_deuda_no_vencida,
                p_antiguedad,
                p_deuda_convenida,
                NULL,                                     --p_estado_cobranza,
                p_numero_serie_ci,
                p_fecha_vencimiento,
                p_canal,
                p_id_convenio,
                p_mensaje,
                p_is_ok);


            OPEN p_recordset FOR
                SELECT *
                  FROM comprobante_convenio_web@LINK_SITIOWEB_SGC10
                 WHERE id_convenio = p_id_convenio;
        ELSIF p_id_empresa = 3
        THEN
            pkg_validaciones_convenio_web.crear_convenio_web@link_sitioweb_sgc03 (
                p_id_servicio,
                p_id_tipo_convenio,
                p_monto_pie,
                p_monto_cuota,
                p_no_cuotas,
                p_total_deuda_conv,
                p_deuda_vencida,
                p_deuda_no_vencida,
                p_antiguedad,
                p_deuda_convenida,
                NULL,                                     --p_estado_cobranza,
                p_numero_serie_ci,
                p_fecha_vencimiento,
                p_canal,
                p_id_convenio,
                p_mensaje,
                p_is_ok);


            OPEN p_recordset FOR
                SELECT *
                  FROM comprobante_convenio_web@link_sitioweb_sgc03
                 WHERE id_convenio = p_id_convenio;
        ELSIF p_id_empresa = 12
        THEN
            pkg_validaciones_convenio_web.crear_convenio_web@link_sitioweb_sgc12 (
                p_id_servicio,
                p_id_tipo_convenio,
                p_monto_pie,
                p_monto_cuota,
                p_no_cuotas,
                p_total_deuda_conv,
                p_deuda_vencida,
                p_deuda_no_vencida,
                p_antiguedad,
                p_deuda_convenida,
                NULL,                                     --p_estado_cobranza,
                p_numero_serie_ci,
                p_fecha_vencimiento,
                p_canal,
                p_id_convenio,
                p_mensaje,
                p_is_ok);


            OPEN p_recordset FOR
                SELECT *
                  FROM comprobante_convenio_web@link_sitioweb_sgc12
                 WHERE id_convenio = p_id_convenio;
        END IF;


        IF p_is_ok = 0
        THEN
            IF p_canal IS NULL OR p_canal = 0
            THEN
                v_canal := 17;                                  -- app  mobile
            ELSE
                v_canal := p_canal;
            END IF;


            INSERT INTO log_usua_metodo_canal (usua_num_cliente,
                                               usua_empresa,
                                               id_metodo,
                                               canal_ingreso,
                                               fecha)
                     VALUES (
                         UPPER (
                                TRIM (p_id_servicio)
                             || '-'
                             || dv_mod11 (p_id_servicio)),
                         p_id_empresa,
                         7,                               --crea convenio web,
                         v_canal,
                         SYSDATE);
        END IF;
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;

    PROCEDURE eliminar_convenio_web (p_id_empresa        NUMBER,
                                     p_id_convenio       NUMBER,
                                     p_canal             NUMBER,
                                     p_mensaje       OUT VARCHAR2,
                                     p_is_ok         OUT NUMBER)
    IS
        v_canal   NUMBER;
    BEGIN
        IF p_id_empresa = 1
        THEN
            pkg_validaciones_convenio_web.eliminar_convenio_web@link_sitioweb_sgc01 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 9
        THEN
            pkg_validaciones_convenio_web.eliminar_convenio_web@link_sitioweb_sgc09 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 10
        THEN
            pkg_validaciones_convenio_web.eliminar_convenio_web@LINK_SITIOWEB_SGC10 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 3
        THEN
            pkg_validaciones_convenio_web.eliminar_convenio_web@link_sitioweb_sgc03 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 12
        THEN
            pkg_validaciones_convenio_web.eliminar_convenio_web@link_sitioweb_sgc12 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        END IF;


        IF p_is_ok = 0
        THEN
            IF p_canal IS NULL OR p_canal = 0
            THEN
                v_canal := 17;                                  -- app  mobile
            ELSE
                v_canal := p_canal;
            END IF;


            INSERT INTO log_usua_metodo_canal (usua_empresa,
                                               id_metodo,
                                               canal_ingreso,
                                               fecha)
                 VALUES (p_id_empresa,
                         8,                                --elimina convenio,
                         v_canal,
                         SYSDATE);
        END IF;
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;

    PROCEDURE consulta_convenio_matico (p_id_empresa              NUMBER,
                                        p_id_servicio             NUMBER,
                                        p_fecha_convenio      OUT VARCHAR2,
                                        p_id_convenio         OUT NUMBER,
                                        p_monto_pie           OUT NUMBER,
                                        p_monto_convenido     OUT NUMBER,
                                        p_n_cuotas_emitidas   OUT NUMBER,
                                        p_no_cuotas           OUT NUMBER,
                                        p_estado              OUT VARCHAR2,
                                        p_mensaje             OUT VARCHAR2,
                                        p_is_ok               OUT NUMBER)
    IS
        v_fecha_convenio   DATE;
    BEGIN
        IF p_id_empresa = 1
        THEN
            pkg_validaciones_convenio_web.consulta_convenio_matico@link_sitioweb_sgc01 (
                p_id_servicio,
                v_fecha_convenio,
                p_id_convenio,
                p_monto_pie,
                p_monto_convenido,
                p_n_cuotas_emitidas,
                p_no_cuotas,
                p_estado,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 9
        THEN
            pkg_validaciones_convenio_web.consulta_convenio_matico@link_sitioweb_sgc09 (
                p_id_servicio,
                v_fecha_convenio,
                p_id_convenio,
                p_monto_pie,
                p_monto_convenido,
                p_n_cuotas_emitidas,
                p_no_cuotas,
                p_estado,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 10
        THEN
            pkg_validaciones_convenio_web.consulta_convenio_matico@LINK_SITIOWEB_SGC10 (
                p_id_servicio,
                v_fecha_convenio,
                p_id_convenio,
                p_monto_pie,
                p_monto_convenido,
                p_n_cuotas_emitidas,
                p_no_cuotas,
                p_estado,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 3
        THEN
            pkg_validaciones_convenio_web.consulta_convenio_matico@link_sitioweb_sgc03 (
                p_id_servicio,
                v_fecha_convenio,
                p_id_convenio,
                p_monto_pie,
                p_monto_convenido,
                p_n_cuotas_emitidas,
                p_no_cuotas,
                p_estado,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 12
        THEN
            pkg_validaciones_convenio_web.consulta_convenio_matico@link_sitioweb_sgc12 (
                p_id_servicio,
                v_fecha_convenio,
                p_id_convenio,
                p_monto_pie,
                p_monto_convenido,
                p_n_cuotas_emitidas,
                p_no_cuotas,
                p_estado,
                p_mensaje,
                p_is_ok);
        END IF;

        p_fecha_convenio := TO_CHAR (v_fecha_convenio, 'dd/mm/yyyy');
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;

    PROCEDURE elimina_convenio_matico (p_id_empresa        NUMBER,
                                       p_id_convenio       NUMBER,
                                       p_mensaje       OUT VARCHAR2,
                                       p_is_ok         OUT NUMBER)
    IS
    BEGIN
        IF p_id_empresa = 1
        THEN
            pkg_validaciones_convenio_web.elimina_convenio_matico@link_sitioweb_sgc01 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 9
        THEN
            pkg_validaciones_convenio_web.elimina_convenio_matico@link_sitioweb_sgc09 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 10
        THEN
            pkg_validaciones_convenio_web.elimina_convenio_matico@LINK_SITIOWEB_SGC10 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 3
        THEN
            pkg_validaciones_convenio_web.elimina_convenio_matico@link_sitioweb_sgc03 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        ELSIF p_id_empresa = 12
        THEN
            pkg_validaciones_convenio_web.elimina_convenio_matico@link_sitioweb_sgc12 (
                p_id_convenio,
                p_mensaje,
                p_is_ok);
        END IF;
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;

    PROCEDURE consulta_tipo_convenio (p_id_empresa        NUMBER,
                                      p_id_servicio       NUMBER,
                                      cur             OUT T_CURSOR,
                                      p_is_ok         OUT NUMBER,
                                      p_mensaje       OUT VARCHAR2)
    IS
        p_deuda                    NUMBER;
        p_fecha                    DATE;
        p_id_tipo_servicio         NUMBER;
        p_id_clasp_tipo_convenio   NUMBER;
    BEGIN
        p_is_ok := 0;
        p_mensaje := 'Error';

        IF p_id_empresa = 1
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@link_sitioweb_sgc01 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            -- p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@link_sitioweb_sgc01 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                    SELECT id_tipo_convenio, nom_tipo_convenio
                      FROM tipo_convenio@link_sitioweb_sgc01,
                           moneda@link_sitioweb_sgc01,
                           tipo_deuda@link_sitioweb_sgc01,
                           tipo_cargo@link_sitioweb_sgc01
                     WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                           -- AND tipo_convenio.fecha_inicio <= p_fecha
                           -- AND tipo_convenio.fecha_fin >= p_fecha
                           AND tipo_convenio.id_tipo_deuda =
                               tipo_deuda.id_tipo_deuda
                           AND b_cheque = 0
                           AND tipo_deuda.cargo_interes =
                               tipo_cargo.id_tipo_cargo(+)
                           AND tipo_convenio.b_activo = 1
                           AND tipo_convenio.b_cheque = 0
                           AND tipo_convenio.deuda_min < p_deuda
                           AND tipo_convenio.deuda_max >= p_deuda
                           --AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                           AND (   tipo_convenio.id_tipo_servicio =
                                   p_id_tipo_servicio
                                OR tipo_convenio.id_tipo_servicio = 999)
                           --    AND tipo_convenio.id_clasp_tipo_convenio = p_id_clasp_tipo_convenio
                           AND id_tipo_convenio IN
                                   (SELECT B_ACTION
                                      FROM tablas@link_sitioweb_sgc01
                                     WHERE cod_tabla = 2990);

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;


        IF p_id_empresa = 9
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@link_sitioweb_sgc09 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            --  p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@link_sitioweb_sgc09 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                    SELECT id_tipo_convenio, nom_tipo_convenio
                      FROM tipo_convenio@link_sitioweb_sgc09,
                           moneda@link_sitioweb_sgc09,
                           tipo_deuda@link_sitioweb_sgc09,
                           tipo_cargo@link_sitioweb_sgc09
                     WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                           --  AND tipo_convenio.fecha_inicio <= p_fecha
                           --  AND tipo_convenio.fecha_fin >= p_fecha
                           AND tipo_convenio.id_tipo_deuda =
                               tipo_deuda.id_tipo_deuda
                           AND b_cheque = 0
                           AND tipo_deuda.cargo_interes =
                               tipo_cargo.id_tipo_cargo(+)
                           AND tipo_convenio.b_activo = 1
                           AND tipo_convenio.b_cheque = 0
                           AND tipo_convenio.deuda_min < p_deuda
                           AND tipo_convenio.deuda_max >= p_deuda
                           --AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                           AND (   tipo_convenio.id_tipo_servicio =
                                   p_id_tipo_servicio
                                OR tipo_convenio.id_tipo_servicio = 999)
                           --   AND tipo_convenio.id_clasp_tipo_convenio = p_id_clasp_tipo_convenio
                           AND id_tipo_convenio IN
                                   (SELECT B_ACTION
                                      FROM tablas@link_sitioweb_sgc09
                                     WHERE cod_tabla = 2990);

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;

        IF p_id_empresa = 10
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@LINK_SITIOWEB_SGC10 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            --  p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@LINK_SITIOWEB_SGC10 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                    SELECT id_tipo_convenio, nom_tipo_convenio
                      FROM tipo_convenio@LINK_SITIOWEB_SGC10,
                           moneda@LINK_SITIOWEB_SGC10,
                           tipo_deuda@LINK_SITIOWEB_SGC10,
                           tipo_cargo@LINK_SITIOWEB_SGC10
                     WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                           --  AND tipo_convenio.fecha_inicio <= p_fecha
                           --  AND tipo_convenio.fecha_fin >= p_fecha
                           AND tipo_convenio.id_tipo_deuda =
                               tipo_deuda.id_tipo_deuda
                           AND b_cheque = 0
                           AND tipo_deuda.cargo_interes =
                               tipo_cargo.id_tipo_cargo(+)
                           AND tipo_convenio.b_activo = 1
                           AND tipo_convenio.b_cheque = 0
                           AND tipo_convenio.deuda_min < p_deuda
                           AND tipo_convenio.deuda_max >= p_deuda
                           --AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                           AND (   tipo_convenio.id_tipo_servicio =
                                   p_id_tipo_servicio
                                OR tipo_convenio.id_tipo_servicio = 999)
                           --   AND tipo_convenio.id_clasp_tipo_convenio = p_id_clasp_tipo_convenio
                           AND id_tipo_convenio IN
                                   (SELECT B_ACTION
                                      FROM tablas@LINK_SITIOWEB_SGC10
                                     WHERE cod_tabla = 2990);

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;


        IF p_id_empresa = 3
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@link_sitioweb_sgc03 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            -- p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@link_sitioweb_sgc03 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                    SELECT id_tipo_convenio, nom_tipo_convenio
                      FROM tipo_convenio@link_sitioweb_sgc03,
                           moneda@link_sitioweb_sgc03,
                           tipo_deuda@link_sitioweb_sgc03,
                           tipo_cargo@link_sitioweb_sgc03
                     WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                           -- AND tipo_convenio.fecha_inicio <= p_fecha
                           --  AND tipo_convenio.fecha_fin >= p_fecha
                           AND tipo_convenio.id_tipo_deuda =
                               tipo_deuda.id_tipo_deuda
                           AND b_cheque = 0
                           AND tipo_deuda.cargo_interes =
                               tipo_cargo.id_tipo_cargo(+)
                           AND tipo_convenio.b_activo = 1
                           AND tipo_convenio.b_cheque = 0
                           AND tipo_convenio.deuda_min < p_deuda
                           AND tipo_convenio.deuda_max >= p_deuda
                           --AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                           AND (   tipo_convenio.id_tipo_servicio =
                                   p_id_tipo_servicio
                                OR tipo_convenio.id_tipo_servicio = 999)
                           --   AND tipo_convenio.id_clasp_tipo_convenio = p_id_clasp_tipo_convenio
                           AND id_tipo_convenio IN
                                   (SELECT B_ACTION
                                      FROM tablas@link_sitioweb_sgc03
                                     WHERE cod_tabla = 2990);

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;



        IF p_id_empresa = 12
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@link_sitioweb_sgc12 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            --  p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@link_sitioweb_sgc12 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                    SELECT id_tipo_convenio, nom_tipo_convenio
                      FROM tipo_convenio@link_sitioweb_sgc12,
                           moneda@link_sitioweb_sgc12,
                           tipo_deuda@link_sitioweb_sgc12,
                           tipo_cargo@link_sitioweb_sgc12
                     WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                           --  AND tipo_convenio.fecha_inicio <= p_fecha
                           --  AND tipo_convenio.fecha_fin >= p_fecha
                           AND tipo_convenio.id_tipo_deuda =
                               tipo_deuda.id_tipo_deuda
                           AND b_cheque = 0
                           AND tipo_deuda.cargo_interes =
                               tipo_cargo.id_tipo_cargo(+)
                           AND tipo_convenio.b_activo = 1
                           AND tipo_convenio.b_cheque = 0
                           AND tipo_convenio.deuda_min < p_deuda
                           AND tipo_convenio.deuda_max >= p_deuda
                           --  AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                           AND (   tipo_convenio.id_tipo_servicio =
                                   p_id_tipo_servicio
                                OR tipo_convenio.id_tipo_servicio = 999)
                           AND id_tipo_convenio IN
                                   (SELECT B_ACTION
                                      FROM tablas@link_sitioweb_sgc12
                                     WHERE cod_tabla = 2990);

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;


    PROCEDURE solicitud_crear_convenio_cyr (
        p_id_empresa                NUMBER,
        p_id_servicio               NUMBER,
        p_canal                     NUMBER,
        p_id_tipo_convenio_in       NUMBER,
        p_crear_convenio        OUT NUMBER,
        p_id_tipo_convenio      OUT NUMBER,
        p_pedir_pie             OUT NUMBER,
        p_total_deuda_conv      OUT NUMBER,
        p_pie_minimo            OUT NUMBER,
        p_pie_maximo            OUT NUMBER,
        p_deuda_vencida         OUT NUMBER,
        p_deuda_no_vencida      OUT NUMBER,
        p_antiguedad            OUT NUMBER,
        p_deuda_convenida       OUT NUMBER,
        p_deuda_cobranza        OUT NUMBER,
        p_mensaje               OUT VARCHAR2,
        p_is_ok                 OUT NUMBER)
    IS
        p_cont    NUMBER := 0;
        v_canal   NUMBER;
    BEGIN
        IF p_id_empresa = 1
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC01
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio_CYR@link_sitioweb_sgc01 ( --CAMBIAR A  CYR
                    p_id_servicio,
                    p_id_tipo_convenio_in,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        ELSIF p_id_empresa = 9
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC09
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio_CYR@link_sitioweb_sgc09 (
                    p_id_servicio,
                    p_id_tipo_convenio_in,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        ELSIF p_id_empresa = 10
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC10
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio_CYR@LINK_SITIOWEB_SGC10 (
                    p_id_servicio,
                    p_id_tipo_convenio_in,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        ELSIF p_id_empresa = 3
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC03
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio_CYR@link_sitioweb_sgc03 (
                    p_id_servicio,
                    p_id_tipo_convenio_in,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        ELSIF p_id_empresa = 12
        THEN
            SELECT COUNT (*)
              INTO p_cont
              FROM RELACION_FACT_AGRUPADA@LINK_SITIOWEB_SGC12
             WHERE id_servicio = p_id_servicio;

            IF p_cont > 0
            THEN
                p_is_ok := 1;
                p_mensaje :=
                    'Estimado Cliente: Las condiciones actuales de tu servicio no permiten la suscripción de convenios a través de este medio. Para mayores antecedentes consulta con un ejecutivo de Atención de Clientes.';
            ELSE
                pkg_validaciones_convenio_web.solicitud_crear_convenio_CYR@link_sitioweb_sgc12 ( --CAMBIAR A  CYR
                    p_id_servicio,
                    p_id_tipo_convenio_in,
                    p_crear_convenio,
                    p_id_tipo_convenio,
                    p_pedir_pie,
                    p_total_deuda_conv,
                    p_pie_minimo,
                    p_pie_maximo,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    p_deuda_cobranza,
                    p_mensaje,
                    p_is_ok);
            END IF;
        END IF;


        IF p_is_ok = 0
        THEN
            IF p_canal IS NULL OR p_canal = 0
            THEN
                v_canal := 17;                                  -- app  mobile
            ELSE
                v_canal := p_canal;
            END IF;


            INSERT INTO log_usua_metodo_canal (usua_num_cliente,
                                               usua_empresa,
                                               id_metodo,
                                               canal_ingreso,
                                               fecha)
                     VALUES (
                         UPPER (
                                TRIM (p_id_servicio)
                             || '-'
                             || dv_mod11 (p_id_servicio)),
                         p_id_empresa,
                         6,                         --solicitud crea convenio,
                         v_canal,
                         SYSDATE);
        END IF;
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;


    PROCEDURE crea_convenio_web_CYR (p_id_empresa              NUMBER,
                                     p_id_servicio             NUMBER,
                                     p_id_tipo_convenio        NUMBER,
                                     p_monto_pie               NUMBER,
                                     p_monto_cuota             NUMBER,
                                     p_no_cuotas               NUMBER,
                                     p_total_deuda_conv        NUMBER,
                                     p_deuda_vencida           NUMBER,
                                     p_deuda_no_vencida        NUMBER,
                                     p_antiguedad              NUMBER,
                                     p_deuda_convenida         NUMBER,
                                     p_numero_serie_ci         VARCHAR2,
                                     p_fecha_vencimiento       DATE,
                                     p_canal                   NUMBER,
                                     p_nombre_apellido         VARCHAR2,
                                     p_rut                     NUMBER,
                                     p_telefono                NUMBER,
                                     p_id_convenio         OUT NUMBER,
                                     p_recordset           OUT SYS_REFCURSOR,
                                     p_mensaje             OUT VARCHAR2,
                                     p_is_ok               OUT NUMBER)
    IS
        v_canal    NUMBER;
        V_CONTAR   NUMBER;
    BEGIN
        BEGIN
            SELECT COUNT (*)
              INTO V_CONTAR
              FROM sitioweb_2.datos_convenio_web
             WHERE     ID_EMPRESA = p_id_empresa
                   AND id_servicio = p_id_servicio
                   AND ID_TIPO_CONVENIO = p_ID_TIPO_CONVENIO
                   AND NO_CUOTAS = p_NO_CUOTAS
                   AND DEUDA_CONVENIDA = p_DEUDA_CONVENIDA;
        EXCEPTION
            WHEN OTHERS
            THEN
                V_CONTAR := 0;
                p_is_ok := 0;
                p_mensaje := 'Error ya existe un convenio';
        END;


        IF V_CONTAR = 0
        THEN
            BEGIN
                INSERT INTO sitioweb_2.datos_convenio_web (ID_EMPRESA,
                                                           ID_SERVICIO,
                                                           ID_TIPO_CONVENIO,
                                                           MONTO_PIE,
                                                           MONTO_CUOTA,
                                                           NO_CUOTAS,
                                                           TOTAL_DEUDA_CONV,
                                                           DEUDA_VENCIDA,
                                                           DEUDA_NO_VENCIDA,
                                                           ANTIGUEDAD,
                                                           DEUDA_CONVENIDA,
                                                           NUMERO_SERIE_CI,
                                                           FECHA_VENCIMIENTO,
                                                           CANAL,
                                                           NOMBRE_APELLIDO,
                                                           RUT,
                                                           TELEFONO)
                     VALUES (p_id_empresa,
                             p_id_servicio,
                             p_id_tipo_convenio,
                             p_monto_pie,
                             p_monto_cuota,
                             p_no_cuotas,
                             p_total_deuda_conv,
                             p_deuda_vencida,
                             p_deuda_no_vencida,
                             p_antiguedad,
                             p_deuda_convenida,
                             p_numero_serie_ci,
                             p_fecha_vencimiento,
                             p_canal,
                             p_nombre_apellido,
                             p_rut,
                             p_telefono);

                COMMIT;
            EXCEPTION
                WHEN OTHERS
                THEN
                    ROLLBACK;
                    NULL;
            END;



            IF p_id_empresa = 1
            THEN
                pkg_validaciones_convenio_web.crear_convenio_web@link_sitioweb_sgc01 (
                    p_id_servicio,
                    p_id_tipo_convenio,
                    p_monto_pie,
                    p_monto_cuota,
                    p_no_cuotas,
                    p_total_deuda_conv,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    NULL,                                 --p_estado_cobranza,
                    p_numero_serie_ci,
                    p_fecha_vencimiento,
                    p_canal,
                    p_id_convenio,
                    p_mensaje,
                    p_is_ok);

                INSERT INTO SITIOWEB_2.LOG_USUA_METODO_CANAL_ERROR (
                                USUA_CODIGO,
                                USUA_EMPRESA,
                                CANAL_INGRESO,
                                ID_METODO,
                                FECHA,
                                MENSAJE)
                     VALUES (p_id_servicio,
                             p_id_empresa,
                             p_canal,
                             p_id_convenio,
                             SYSDATE,
                             p_mensaje);


                OPEN p_recordset FOR
                    SELECT *
                      FROM comprobante_convenio_web@link_sitioweb_sgc01
                     WHERE id_convenio = p_id_convenio;
            ELSIF p_id_empresa = 9
            THEN
                pkg_validaciones_convenio_web.crear_convenio_web@link_sitioweb_sgc09 (
                    p_id_servicio,
                    p_id_tipo_convenio,
                    p_monto_pie,
                    p_monto_cuota,
                    p_no_cuotas,
                    p_total_deuda_conv,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    NULL,                                 --p_estado_cobranza,
                    p_numero_serie_ci,
                    p_fecha_vencimiento,
                    p_canal,
                    p_id_convenio,
                    p_mensaje,
                    p_is_ok);

                INSERT INTO SITIOWEB_2.LOG_USUA_METODO_CANAL_ERROR (
                                USUA_CODIGO,
                                USUA_EMPRESA,
                                CANAL_INGRESO,
                                ID_METODO,
                                FECHA,
                                MENSAJE)
                     VALUES (p_id_servicio,
                             p_id_empresa,
                             p_canal,
                             p_id_convenio,
                             SYSDATE,
                             p_mensaje);


                OPEN p_recordset FOR
                    SELECT *
                      FROM comprobante_convenio_web@link_sitioweb_sgc09
                     WHERE id_convenio = p_id_convenio;
            ELSIF p_id_empresa = 10
            THEN
                pkg_validaciones_convenio_web.crear_convenio_web@LINK_SITIOWEB_SGC10 (
                    p_id_servicio,
                    p_id_tipo_convenio,
                    p_monto_pie,
                    p_monto_cuota,
                    p_no_cuotas,
                    p_total_deuda_conv,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    NULL,                                 --p_estado_cobranza,
                    p_numero_serie_ci,
                    p_fecha_vencimiento,
                    p_canal,
                    p_id_convenio,
                    p_mensaje,
                    p_is_ok);

                INSERT INTO SITIOWEB_2.LOG_USUA_METODO_CANAL_ERROR (
                                USUA_CODIGO,
                                USUA_EMPRESA,
                                CANAL_INGRESO,
                                ID_METODO,
                                FECHA,
                                MENSAJE)
                     VALUES (p_id_servicio,
                             p_id_empresa,
                             p_canal,
                             p_id_convenio,
                             SYSDATE,
                             p_mensaje);


                OPEN p_recordset FOR
                    SELECT *
                      FROM comprobante_convenio_web@LINK_SITIOWEB_SGC10
                     WHERE id_convenio = p_id_convenio;
            ELSIF p_id_empresa = 3
            THEN
                pkg_validaciones_convenio_web.crear_convenio_web@link_sitioweb_sgc03 (
                    p_id_servicio,
                    p_id_tipo_convenio,
                    p_monto_pie,
                    p_monto_cuota,
                    p_no_cuotas,
                    p_total_deuda_conv,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    NULL,                                 --p_estado_cobranza,
                    p_numero_serie_ci,
                    p_fecha_vencimiento,
                    p_canal,
                    p_id_convenio,
                    p_mensaje,
                    p_is_ok);

                INSERT INTO SITIOWEB_2.LOG_USUA_METODO_CANAL_ERROR (
                                USUA_CODIGO,
                                USUA_EMPRESA,
                                CANAL_INGRESO,
                                ID_METODO,
                                FECHA,
                                MENSAJE)
                     VALUES (p_id_servicio,
                             p_id_empresa,
                             p_canal,
                             p_id_convenio,
                             SYSDATE,
                             p_mensaje);

                OPEN p_recordset FOR
                    SELECT *
                      FROM comprobante_convenio_web@link_sitioweb_sgc03
                     WHERE id_convenio = p_id_convenio;
            ELSIF p_id_empresa = 12
            THEN
                pkg_validaciones_convenio_web.crear_convenio_web@link_sitioweb_sgc12 (
                    p_id_servicio,
                    p_id_tipo_convenio,
                    p_monto_pie,
                    p_monto_cuota,
                    p_no_cuotas,
                    p_total_deuda_conv,
                    p_deuda_vencida,
                    p_deuda_no_vencida,
                    p_antiguedad,
                    p_deuda_convenida,
                    NULL,                                 --p_estado_cobranza,
                    p_numero_serie_ci,
                    p_fecha_vencimiento,
                    p_canal,
                    p_id_convenio,
                    p_mensaje,
                    p_is_ok);


                INSERT INTO SITIOWEB_2.LOG_USUA_METODO_CANAL_ERROR (
                                USUA_CODIGO,
                                USUA_EMPRESA,
                                CANAL_INGRESO,
                                ID_METODO,
                                FECHA,
                                MENSAJE)
                     VALUES (p_id_servicio,
                             p_id_empresa,
                             p_canal,
                             p_id_convenio,
                             SYSDATE,
                             p_mensaje);

                OPEN p_recordset FOR
                    SELECT *
                      FROM comprobante_convenio_web@link_sitioweb_sgc12
                     WHERE id_convenio = p_id_convenio;
            END IF;
        END IF;


        IF p_is_ok = 0
        THEN
            IF p_canal IS NULL OR p_canal = 0
            THEN
                v_canal := 17;                                  -- app  mobile
            ELSE
                v_canal := p_canal;
            END IF;


            INSERT INTO log_usua_metodo_canal (usua_num_cliente,
                                               usua_empresa,
                                               id_metodo,
                                               canal_ingreso,
                                               fecha)
                     VALUES (
                         UPPER (
                                TRIM (p_id_servicio)
                             || '-'
                             || dv_mod11 (p_id_servicio)),
                         p_id_empresa,
                         7,                               --crea convenio web,
                         v_canal,
                         SYSDATE);
        END IF;
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;


    /* Modificación [IJM] 17/10/2022  - Sarche Service SpA
        Mejoras Convenio Sitios WEB
     */

    PROCEDURE consulta_tipo_convenio_texto (p_id_empresa        NUMBER,
                                            p_id_servicio       NUMBER,
                                            cur             OUT T_CURSOR,
                                            p_is_ok         OUT NUMBER,
                                            p_mensaje       OUT VARCHAR2)
    IS
        p_deuda                    NUMBER;
        p_fecha                    DATE;
        p_id_tipo_servicio         NUMBER;
        p_id_clasp_tipo_convenio   NUMBER;
    BEGIN
        p_is_ok := 0;
        p_mensaje := 'Error';

        IF p_id_empresa = 1
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@link_sitioweb_sgc01 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            -- p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@link_sitioweb_sgc01 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                    SELECT tipo_convenio.id_tipo_convenio
                               AS id_tipo_convenio,
                           nom_tipo_convenio
                               AS nom_tipo_convenio,
                           ptc.texto_tipo_convenio
                               AS texto_convenio
                      FROM tipo_convenio@link_sitioweb_sgc01,
                           moneda@link_sitioweb_sgc01,
                           tipo_deuda@link_sitioweb_sgc01,
                           tipo_cargo@link_sitioweb_sgc01,
                           sisweb20_2.parametro_tipo_convenio  ptc
                     WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                           --                    AND tipo_convenio.fecha_inicio <= p_fecha
                           --                    AND tipo_convenio.fecha_fin >= p_fecha
                           AND tipo_convenio.id_tipo_deuda =
                               tipo_deuda.id_tipo_deuda
                           AND b_cheque = 0
                           AND tipo_deuda.cargo_interes =
                               tipo_cargo.id_tipo_cargo(+)
                           AND tipo_convenio.b_activo = 1
                           AND tipo_convenio.b_cheque = 0
                           AND tipo_convenio.deuda_min < p_deuda
                           AND tipo_convenio.deuda_max >= p_deuda
                           --AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                           AND (   tipo_convenio.id_tipo_servicio =
                                   p_id_tipo_servicio
                                OR tipo_convenio.id_tipo_servicio = 999)
                           AND tipo_convenio.id_clasp_tipo_convenio =
                               p_id_clasp_tipo_convenio
                           AND tipo_convenio.id_tipo_convenio IN
                                   (SELECT B_ACTION
                                      FROM tablas@link_sitioweb_sgc01
                                     WHERE cod_tabla = 2990)
                           AND ptc.id_tipo_convenio =
                               tipo_convenio.id_tipo_convenio;

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;


        IF p_id_empresa = 9
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@link_sitioweb_sgc09 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            --  p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@link_sitioweb_sgc09 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                      SELECT tipo_convenio.id_tipo_convenio
                                 AS id_tipo_convenio,
                             nom_tipo_convenio
                                 AS nom_tipo_convenio,
                             ptc.texto_tipo_convenio
                                 AS texto_convenio
                        FROM tipo_convenio@link_sitioweb_sgc09,
                             moneda@link_sitioweb_sgc09,
                             tipo_deuda@link_sitioweb_sgc09,
                             tipo_cargo@link_sitioweb_sgc09,
                             sisweb20_2.parametro_tipo_convenio ptc
                       WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                             --  AND tipo_convenio.fecha_inicio <= p_fecha
                             --  AND tipo_convenio.fecha_fin >= p_fecha
                             AND tipo_convenio.id_tipo_deuda =
                                 tipo_deuda.id_tipo_deuda
                             AND b_cheque = 0
                             AND tipo_deuda.cargo_interes =
                                 tipo_cargo.id_tipo_cargo(+)
                             AND tipo_convenio.b_activo = 1
                             AND tipo_convenio.b_cheque = 0
                             AND tipo_convenio.deuda_min < p_deuda
                             AND tipo_convenio.deuda_max >= p_deuda
                             --AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                             AND (   tipo_convenio.id_tipo_servicio =
                                     p_id_tipo_servicio
                                  OR tipo_convenio.id_tipo_servicio = 999)
                             AND tipo_convenio.id_clasp_tipo_convenio =
                                 p_id_clasp_tipo_convenio
                             AND tipo_convenio.id_tipo_convenio IN
                                     (SELECT B_ACTION
                                        FROM tablas@link_sitioweb_sgc09
                                       WHERE cod_tabla = 2990)
                             AND ptc.id_tipo_convenio =
                                 tipo_convenio.id_tipo_convenio
                    GROUP BY tipo_convenio.id_tipo_convenio,
                             nom_tipo_convenio,
                             ptc.texto_tipo_convenio;

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;


        IF p_id_empresa = 10
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@LINK_SITIOWEB_SGC10 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            --  p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@LINK_SITIOWEB_SGC10 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                      SELECT tipo_convenio.id_tipo_convenio
                                 AS id_tipo_convenio,
                             nom_tipo_convenio
                                 AS nom_tipo_convenio,
                             ptc.texto_tipo_convenio
                                 AS texto_convenio
                        FROM tipo_convenio@LINK_SITIOWEB_SGC10,
                             moneda@LINK_SITIOWEB_SGC10,
                             tipo_deuda@LINK_SITIOWEB_SGC10,
                             tipo_cargo@LINK_SITIOWEB_SGC10,
                             sisweb20_2.parametro_tipo_convenio ptc
                       WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                             --  AND tipo_convenio.fecha_inicio <= p_fecha
                             --  AND tipo_convenio.fecha_fin >= p_fecha
                             AND tipo_convenio.id_tipo_deuda =
                                 tipo_deuda.id_tipo_deuda
                             AND b_cheque = 0
                             AND tipo_deuda.cargo_interes =
                                 tipo_cargo.id_tipo_cargo(+)
                             AND tipo_convenio.b_activo = 1
                             AND tipo_convenio.b_cheque = 0
                             AND tipo_convenio.deuda_min < p_deuda
                             AND tipo_convenio.deuda_max >= p_deuda
                             --AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                             AND (   tipo_convenio.id_tipo_servicio =
                                     p_id_tipo_servicio
                                  OR tipo_convenio.id_tipo_servicio = 999)
                             AND tipo_convenio.id_clasp_tipo_convenio =
                                 p_id_clasp_tipo_convenio
                             AND tipo_convenio.id_tipo_convenio IN
                                     (SELECT B_ACTION
                                        FROM tablas@link_sitioweb_sgc09
                                       WHERE cod_tabla = 2990)
                             AND ptc.id_tipo_convenio =
                                 tipo_convenio.id_tipo_convenio
                    GROUP BY tipo_convenio.id_tipo_convenio,
                             nom_tipo_convenio,
                             ptc.texto_tipo_convenio;

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;



        IF p_id_empresa = 3
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@link_sitioweb_sgc03 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            -- p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@link_sitioweb_sgc03 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                    SELECT tipo_convenio.id_tipo_convenio
                               AS id_tipo_convenio,
                           nom_tipo_convenio
                               AS nom_tipo_convenio,
                           ptc.texto_tipo_convenio
                               AS texto_convenio
                      FROM tipo_convenio@link_sitioweb_sgc03,
                           moneda@link_sitioweb_sgc03,
                           tipo_deuda@link_sitioweb_sgc03,
                           tipo_cargo@link_sitioweb_sgc03,
                           sisweb20_2.parametro_tipo_convenio  ptc
                     WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                           -- AND tipo_convenio.fecha_inicio <= p_fecha
                           -- AND tipo_convenio.fecha_fin >= p_fecha
                           AND tipo_convenio.id_tipo_deuda =
                               tipo_deuda.id_tipo_deuda
                           AND b_cheque = 0
                           AND tipo_deuda.cargo_interes =
                               tipo_cargo.id_tipo_cargo(+)
                           AND tipo_convenio.b_activo = 1
                           AND tipo_convenio.b_cheque = 0
                           AND tipo_convenio.deuda_min < p_deuda
                           AND tipo_convenio.deuda_max >= p_deuda
                           --AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                           AND (   tipo_convenio.id_tipo_servicio =
                                   p_id_tipo_servicio
                                OR tipo_convenio.id_tipo_servicio = 999)
                           AND tipo_convenio.id_clasp_tipo_convenio =
                               p_id_clasp_tipo_convenio
                           AND tipo_convenio.id_tipo_convenio IN
                                   (SELECT B_ACTION
                                      FROM tablas@link_sitioweb_sgc03
                                     WHERE cod_tabla = 2990)
                           AND ptc.id_tipo_convenio =
                               tipo_convenio.id_tipo_convenio;

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;



        IF p_id_empresa = 12
        THEN
            p_fecha := TRUNC (SYSDATE);

            SELECT SP_DEVUELVE_ULTIMO_SALDO_EX@link_sitioweb_sgc12 (
                       p_id_servicio,
                       p_fecha)
              INTO p_deuda
              FROM DUAL;

            --BORRAR
            --  p_deuda:=100000;

            SELECT s.id_tipo_servicio, s.ID_CLASP_SERVICIO
              INTO p_id_tipo_servicio, p_id_clasp_tipo_convenio
              FROM servicio@link_sitioweb_sgc12 s
             WHERE id_servicio = p_id_servicio;

            BEGIN
                OPEN cur FOR
                    SELECT tipo_convenio.id_tipo_convenio
                               AS id_tipo_convenio,
                           nom_tipo_convenio
                               AS nom_tipo_convenio,
                           ptc.texto_tipo_convenio
                               AS texto_convenio
                      FROM tipo_convenio@link_sitioweb_sgc12,
                           moneda@link_sitioweb_sgc12,
                           tipo_deuda@link_sitioweb_sgc12,
                           tipo_cargo@link_sitioweb_sgc12,
                           sisweb20_2.parametro_tipo_convenio  ptc
                     WHERE     tipo_convenio.id_moneda = moneda.id_moneda
                           --                    AND tipo_convenio.fecha_inicio <= p_fecha
                           --                    AND tipo_convenio.fecha_fin >= p_fecha
                           AND tipo_convenio.id_tipo_deuda =
                               tipo_deuda.id_tipo_deuda
                           AND b_cheque = 0
                           AND tipo_deuda.cargo_interes =
                               tipo_cargo.id_tipo_cargo(+)
                           AND tipo_convenio.b_activo = 1
                           AND tipo_convenio.b_cheque = 0
                           AND tipo_convenio.deuda_min < p_deuda
                           AND tipo_convenio.deuda_max >= p_deuda
                           --                    AND tipo_convenio.id_tipo_servicio = p_id_tipo_servicio
                           AND (   tipo_convenio.id_tipo_servicio =
                                   p_id_tipo_servicio
                                OR tipo_convenio.id_tipo_servicio = 999)
                           AND tipo_convenio.id_clasp_tipo_convenio =
                               p_id_clasp_tipo_convenio
                           AND tipo_convenio.id_tipo_convenio IN
                                   (SELECT B_ACTION
                                      FROM tablas@link_sitioweb_sgc12
                                     WHERE cod_tabla = 2990)
                           AND ptc.id_tipo_convenio =
                               tipo_convenio.id_tipo_convenio;

                p_is_ok := 1;
                p_mensaje := NULL;
            EXCEPTION
                WHEN OTHERS
                THEN
                    p_is_ok := 0;
                    p_mensaje := 'Error';
            END;
        END IF;
    EXCEPTION
        WHEN OTHERS
        THEN
            ROLLBACK;
            RAISE;
    END;
END;
/


GRANT EXECUTE, DEBUG
    ON SITIOWEB_2.METODOS_SGC20_CONVENIO
    TO ROL_ADMIN_SITIOWEB_2;

GRANT EXECUTE, DEBUG
    ON SITIOWEB_2.METODOS_SGC20_CONVENIO
    TO ROL_CONS_SITIOWEB_2;