{% snapshot snapshot_productos %}
{{
    config(
        target_schema='snapshots',
        unique_key='"ProductoID"',
        strategy='check',
        check_cols=['"Nombre"', '"Descripcion"', '"Precio"', '"Stock"', '"CategoriaID"']
    )
}}

SELECT * FROM {{ ref('stg_productos') }}

{% endsnapshot %}