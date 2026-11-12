# Modelo entidad-relación

Base de datos `agua_cocacola` (MySQL). Fuente: `sql/schema.sql`. GitHub dibuja el diagrama automáticamente.

```mermaid
erDiagram
    PROCESOS ||--o{ CONSUMOS : registra
    PROCESOS ||--o{ REFERENCIAS : tiene
    PROCESOS ||--o{ ALERTAS : genera

    PROCESOS {
        int id PK
        varchar nombre UK "lavado_envases, refrigeracion..."
    }
    CONSUMOS {
        int id PK
        int proceso_id FK
        date fecha
        decimal consumo_m3
    }
    REFERENCIAS {
        int id PK
        int proceso_id FK
        char mes "AAAA-MM"
        decimal valor_m3
    }
    ALERTAS {
        int id PK
        int proceso_id FK
        char periodo "AAAA-MM"
        decimal desviacion_pct
        enum nivel "informativa, preventiva, critica"
    }
```

## Restricciones

| Tabla | Restricción | Para qué |
| --- | --- | --- |
| procesos | `nombre` único | Un solo registro por proceso |
| consumos | único (`proceso_id`, `fecha`) | HU-09: no guardar dos veces el mismo registro |
| referencias | único (`proceso_id`, `mes`) | Una sola referencia por proceso y mes |

La tabla `alertas` se llena en la HU-05 (Sprint 3).
