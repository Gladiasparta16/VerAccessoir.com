Integration notes for admin: how to set category and type when adding products

Requirements for backend/admin to support these new pages:

- Each product must expose two fields: `gender` and `type`.
  - `gender`: one of `men`, `women`, `kids`.
  - `type`: one of `solaire`, `optiques`.

- Suggested API payload when creating/updating a product (JSON):

  {
    "name": "Lunettes Exemple",
    "price": 15000,
    "image": "https://...",
    "gender": "men",
    "type": "solaire",
    "featured": false
  }

- Admin UI: add two select fields when adding/editing a product:
  - `Genre` (select: Homme / Femme / Enfant) mapped to `gender`
  - `Type` (select: Solaire / Optiques) mapped to `type`

- The frontend pages in `FRONTEND/pages/shop/` are static and read simulated product lists.
  To make them dynamic, ensure the product listing API returns `gender` and `type` and the frontend JS filters by those values.
