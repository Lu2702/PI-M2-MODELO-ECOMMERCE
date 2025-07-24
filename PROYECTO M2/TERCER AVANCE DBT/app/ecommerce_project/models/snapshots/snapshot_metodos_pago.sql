{% snapshot snapshot_metodos_pago %}
{{
    config(
        target_schema='snapshots',
        unique_key='"MetodoPagoID"',
        strategy='check',
        check_cols=['"Nombre"', '"Descripcion"']
    )
}}

SELECT * FROM {{ ref('stg_metodos_pago') }}

{% endsnapshot %}