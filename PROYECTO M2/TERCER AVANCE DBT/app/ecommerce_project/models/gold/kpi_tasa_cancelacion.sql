{{ config(materialized='table') }}

SELECT
    COUNT(*) AS "TotalOrdenes",
    SUM("EsCancelada") AS "TotalCanceladas",
    SUM("EsCancelada") * 1.0 / COUNT(*) AS "TasaCancelacion"
FROM {{ ref('fct_ordenes') }}