erDiagram
    User ||--o{ Place : owns
    User ||--o{ Review : writes
    Place ||--o{ Review : has
    Place }|--|| User : owned_by
    Place }o--o{ Amenity : has
    Review }|--|| User : written_by
    Review }|--|| Place : about

    User {
        uuid id
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    Place {
        uuid id
        string title
        text description
        decimal price
        float latitude
        float longitude
        uuid owner_id
        datetime created_at
        datetime updated_at
    }

    Review {
        uuid id
        text text
        integer rating
        uuid user_id
        uuid place_id
        datetime created_at
        datetime updated_at
    }

    Amenity {
        uuid id
        string name
        datetime created_at
        datetime updated_at
    }

    place_amenity {
        uuid place_id
        uuid amenity_id
    }
