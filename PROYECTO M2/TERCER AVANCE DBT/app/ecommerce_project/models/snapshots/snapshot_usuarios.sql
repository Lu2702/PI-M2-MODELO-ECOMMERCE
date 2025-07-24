{% snapshot snapshot_usuarios %}
{{
    config(
        target_schema='snapshots',
        unique_key='"UsuarioID"',
        strategy='check',
        check_cols=['"Nombre"', '"Apellido"', '"dni"', '"Email"', '"Contraseña"', '"FechaRegistro"']
    )
}}

SELECT * FROM {{ ref('stg_usuarios') }}

{% endsnapshot %}