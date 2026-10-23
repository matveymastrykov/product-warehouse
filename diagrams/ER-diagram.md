erDiagram
    categories {
        INTEGER category_id PK
        TEXT name
    }

    suppliers {
        INTEGER supplier_id PK
        TEXT name
        TEXT phone
    }

    products {
        INTEGER product_id PK
        TEXT name
        TEXT unit
        INTEGER category_id FK
    }

    deliveries {
        INTEGER delivery_id PK
        INTEGER supplier_id FK
        TEXT delivery_date
    }

    delivery_items {
        INTEGER item_id PK
        INTEGER delivery_id FK
        INTEGER product_id FK
        INTEGER quantity
        REAL unit_price
        TEXT expiration_date
    }

    writeoffs {
        INTEGER writeoff_id PK
        TEXT writeoff_date
        TEXT reason
    }

    writeoff_items {
        INTEGER writeoff_item_id PK
        INTEGER writeoff_id FK
        INTEGER item_id FK
        INTEGER quantity
    }

    categories ||--o{ products : contains
    suppliers ||--o{ deliveries : supplies
    deliveries ||--o{ delivery_items : includes
    products ||--o{ delivery_items : appears_in
    writeoffs ||--o{ writeoff_items : includes
    delivery_items ||--o{ writeoff_items : written_off