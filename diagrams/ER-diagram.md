```mermaid
erDiagram
    CATEGORIES ||--o{ PRODUCTS : "содержит"
    SUPPLIERS ||--o{ DELIVERIES : "поставляет"
    DELIVERIES ||--o{ DELIVERY_ITEMS : "включает"
    PRODUCTS ||--o{ DELIVERY_ITEMS : "поступает"

    CATEGORIES {
        INTEGER category_id PK
        TEXT name
    }

    SUPPLIERS {
        INTEGER supplier_id PK
        TEXT name
        TEXT phone
    }

    PRODUCTS {
        INTEGER product_id PK
        TEXT name
        TEXT unit
        INTEGER category_id FK
    }

    DELIVERIES {
        INTEGER delivery_id PK
        INTEGER supplier_id FK
        TEXT delivery_date
    }

    DELIVERY_ITEMS {
        INTEGER item_id PK
        INTEGER delivery_id FK
        INTEGER product_id FK
        INTEGER quantity
        REAL unit_price
    }
```