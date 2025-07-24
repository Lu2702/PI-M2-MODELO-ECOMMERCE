{{ config(materialized='table') }}

WITH "UsuariosCarrito" AS (
    SELECT DISTINCT "UsuarioID"
    FROM {{ ref('fct_carrito') }}
),
"UsuariosOrdenes" AS (
    SELECT DISTINCT "UsuarioID"
    FROM {{ ref('fct_ordenes') }}
    WHERE "Estado" IN ('Completado', 'Enviado')
),
"Conteo" AS (
    SELECT 
        COUNT(DISTINCT uc."UsuarioID") AS "UsuariosConCarrito",
        COUNT(DISTINCT uo."UsuarioID") AS "UsuariosConCompra"
    FROM "UsuariosCarrito" uc
    LEFT JOIN "UsuariosOrdenes" uo
        ON uc."UsuarioID" = uo."UsuarioID"
)

SELECT *,
    CASE 
        WHEN "UsuariosConCarrito" > 0 THEN "UsuariosConCompra" * 1.0 / "UsuariosConCarrito"
        ELSE 0 
    END AS "TasaConversion"
FROM "Conteo"
