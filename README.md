# Extremely safe private password manager 🔒

## Setup & Installation 🛠️

-----------

Before you start application you have to configure ``PostgreSQL`` database.

Then run following commands to run your project:

```shell
git clone https://github.com/avadeu/esppm
cd esppm
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

There's one last step before you launch an application which is creating ``.env`` file (or modifying ``.env.example``) in project's root directory.

| :warning: **WARNING**                                                                                         |
|:--------------------------------------------------------------------------------------------------------------|
| Do not use application with default values from ``.env.example`` It will make your application vulnerable.    |

The last step us to launch application. There are two ways to do it.

1.  First one is to configure settings we care about in ``conf.toml`` file and run ``launch.py`` module.
    ```shell
    python launch.py
    ```

2.  Second way is to manually start server using `uvicorn`.
    ```shell
    uvicorn app.api.application:app
    ```

## Project structure&nbsp; 🏗️

------------

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
    ├── utils               - general project utility tools.
    └── application.py      - FastAPI application creation and configuration.
