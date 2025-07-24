{{ config(materialized='table') }}

SELECT
    DATE_TRUNC('month', o."FechaOrden") AS mes,
    SUM(mp."MontoPagado") AS "IngresoMensual",
    SUM(SUM(mp."MontoPagado")) OVER (ORDER BY DATE_TRUNC('month', o."FechaOrden")) AS "IngresoAcumulado"
FROM {{ ref('fct_ordenes') }} o
JOIN {{ ref('fct_ordenes_metodos_pago') }} mp
  ON o."OrdenID" = mp."OrdenID"
WHERE o."Estado" IN ('Completado', 'Enviado')
GROUP BY mes