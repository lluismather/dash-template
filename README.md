
# Plotly Dash Template
This is a template for a dash app with postgres database. It borrows some ideas from other web frameworks, including migration patterns, service providers, directory structure, auth, styling and more to make it easier to get started with dash as a multi page web app. Over the coming weeks/months this template will be updated with more features and improvements in order to make it as modular and flexible to use as possible.

### Setup
- Clone the repository
- Create a virtual environment: `python -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the requirements: `pip install -r requirements.txt`
- Copy the `.env.example` file to `.env` and fill in the necessary details
- Ensure you have a postgres database running and to migrate the database
- Set up the npm packages for tailwind: `npm install` and `npm run build` or `npm run watch`
- Run the application: `python app.py`

### Migrations
- To add migration files: `python manage.py migrate:make create_users_table"
- To apply migrations: `python manage.py migrate:upgrade`
- To drop tables and migrate fresh: `python manage.py migrate:fresh`

### Models
Each model is defined in its own file in the `app/models` directory. This is to keep the models separate and modular. The `db.Model` class is used to define the base model for all models.
- To create a new model, run `python manage.py model:create User users`
- This will create a new model file in the `app/models` directory

### Jobs
Jobs can be defined in the `app/jobs` directory. Any `.py` file in the `jobs` directory will be callable as a job.
- Job files should have a `run` function that is called when the job is run

### Styling
- Tailwind is used for styling. To set up for compiling css run `npm install` in the root directory
- To compile css run `npm run build` or `npm run watch` in the root directory

### Auth
- Auth is handled in the `auth_provider.py` file. This is where you can add your own auth logic

### App
- `python app.py` is the entry point for the application
- This lines up the app_provider.py file, which is where you can add or modify your own app logic
- You can access layouts in `resources/layouts` and components in `resources/components`
- Pages are in the `resources/pages` directory

More docs to come...