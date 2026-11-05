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

