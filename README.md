# Extremely safe private password manager 🔒

## Project structure&nbsp; 🏗️

---------

Files related to application are in the ``app`` or ``tests`` directories.
Application parts are:

    app
    ├── api                 - web related stuff.
    │   ├── db              - db related stuff.
    │   ├── routes          - web routes.
    │   ├── errors          - definition of error handlers.
    │   ├── dependencies    - dependencies for routes definition.
    │   └── models          - database models for application.
    │      ├── domain       - sqlalchemy orm models.
    │      └── schemas      - schemas for using in web routes.
    ├── security            - code related to authentication, security.
    │   └── encryption      - everything related to data encryption.
    ├── utils               - general user utility tools.
    └── application.py      - FastAPI application creation and configuration.
