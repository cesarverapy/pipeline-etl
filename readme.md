
# ETL Pipeline Project

## Description
This project is a simple ETL (Extract, Transform, Load) pipeline built with Python and PostgreSQL.  
It creates a normalized database schema and loads cleaned sales data into two related tables:
- **outlets**
- **products_data**

The script handles duplicates safely using `ON CONFLICT DO NOTHING`.

---

## Project Structure
```
pipeline_etl/
├── dataset/
│   └── cleaned_sales_dataset.csv
├── sql/
│   └── create_table.sql
├── etl.py
├── .env
└── .gitignore
```

---

## How to Run
1. Add your PostgreSQL credentials to `.env`:
```
DB_USER=your_user
DB_PASS=your_password
DB_HOST=your_host
DB_PORT=your_port
DB_NAME=database_name
```
2. Run the ETL script:
```bash
python etl.py
```

---

## Features
- PostgreSQL schema creation
- Duplicate-safe inserts (`ON CONFLICT DO NOTHING`)
- Ready for Power BI or other visualization tools

---

## Future Improvements
- Add Power BI dashboards
- Dockerize the pipeline
- Add unit tests