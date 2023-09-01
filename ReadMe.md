# Build A SAAS with Subdomain in DJANGO using Django-Tenants

## Setup Environment

1. **Create a Virtual Environment:**

    ```bash
    # Windows
    py -3 -m venv env
    # Linux and Mac
    python -m venv env
    ```

2. **Activate the Environment:**

    ```bash
    # Windows
    .\env\Scripts\activate
    # Linux and Mac
    source env/bin/activate
    ```

3. **Install Requirements:**

    ```bash
    pip install -r requirements.txt
    ```

## Database Configuration

4. **Configure Database in Settings.py:**

    In your `settings.py`, add the database configuration for multi-tenancy using Django-Tenants:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': 'DB name',
            'USER': 'postgres',
            'PASSWORD': 'PWD your password',
            'HOST': 'localhost',
            'POST': '5432'
        }
    }
    DATABASE_ROUTERS = (
        'django_tenants.routers.TenantSyncRouter',
    )
    ```

5. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

## Create Models and Admin Interface

6. **Create Models and Register with Admin Interface:**

    Define your models and register them with the admin interface:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```

7. **Collect Static Files:**

    Collect static files to include CKEditor required media files:

    ```bash
    python manage.py collectstatic
    ```

## Populate the Database

8. **Add Content to Your Database:**

    Populate your database with the necessary content.

9. **Create Blog Pages:**

    Use the "Create Blog Page" feature to create multiple subdomains and style them as needed.

## Conclusion

We have set up a SaaS application with subdomain support using Django and Django-Tenants.

For more details and advanced configurations, check the documentation.

---
