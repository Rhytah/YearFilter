# Year Filter API (Django Version)

A Django-based API for filtering Wikimedia Commons files based on the year they were taken. This API is specifically designed to support the Cat-a-lot gadget's year filtering feature.

## Features

- Filter pages by exact year or year range
- Support for both GET and POST requests
- Simulation mode for testing
- Admin interface for data management
- Command-line tools for data import

## API Usage

### Endpoint

```
GET/POST /cat_a_lot_yearfilter
```

### Parameters

- `page_ids`: Comma-separated list of page IDs to filter (required)
- `year`: Return only pages from this exact year (optional)
- `start_year` and `end_year`: Return pages with years between start and end (optional)
- `simulated`: If set to 'true' or '1', returns fake data for testing (optional)

### Examples

```
GET /cat_a_lot_yearfilter?page_ids=123,124,125,126&year=1995
```

Response:
```json
[123, 125]
```

```
GET /cat_a_lot_yearfilter?page_ids=123,124,125,126&start_year=1990&end_year=2000
```

Response:
```json
[123, 125, 126]
```

## Setup

### Prerequisites

- Python 3.8+
- pip
- Docker and Docker Compose (optional, for containerized development)

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Rhytah/YearFilter.git
   cd cat-a-lot-yearfilter
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Docker Setup

1. Build and start the Docker container:
   ```bash
   docker-compose up
   ```

2. To rebuild the image:
   ```bash
   docker-compose build
   ```

3. To view logs:
   ```bash
   docker-compose logs -f
   ```

4. To stop the container:
   ```bash
   docker-compose down
   ```

5. To run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. To create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. To import data:
   ```bash
   docker-compose exec web python manage.py import_data /path/to/data_file.tsv
   ```

This will start the API service on port 8000.

## Management Commands

### Import Data

To import data from a tab-separated file:

```bash
python manage.py import_data /path/to/data_file.tsv
```

For gzipped files:
```bash
python manage.py import_data /path/to/data_file.tsv.gz
```

Optional parameters:
- `--chunk-size`: Number of records to insert in a batch (default: 5000)
- `--keep-existing`: Do not clear existing data before import

## Data Format

The import file should be a tab-separated values file with the following format:

```
page_id year
291 1999
292 1935
293 2004
```

## Deployment to Toolforge

### Preparation

1. Clone the repository on Toolforge:
   ```bash
   git clone https://github.com/Rhytah/YearFilter.git
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure environment variables (create a file named `.env` in the project root):
   ```
   SECRET_KEY=your-secure-secret-key
   DJANGO_DEBUG=False
   ALLOWED_HOSTS=cat-a-lot-yearfilter.toolforge.org
   DJANGO_DB_ENGINE=mysql
   DJANGO_DB_NAME=s12345__yearfilter
   DJANGO_DB_USER=s12345
   ```

### Database Setup

Create a database for the tool using the Toolforge MariaDB service:

1. Connect to the Toolforge database:
   ```bash
   sql <your-database-name>
   ```

2. The Django migrations will create the needed tables.



### Database Maintenance

Use the Django management command to run database maintenance tasks:

```bash
python manage.py dbshell
```
### Run tests
```bash
python manage.py test
```
#### With Coverage
```bash
coverage run --source='.' manage.py test api
coverage report
```
![Coverage](https://img.shields.io/badge/coverage-59%25-brightgreen)
