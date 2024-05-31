## Initial Setup

For local deployment, follow these instructions:

1. **Repository Cloning**: Use the command below to clone the app repository to your machine:
   ```
   git clone https://github.com/dmm1/Ecosphere.git
   ```

2. **Dependency Installation**: Within the project folder, install necessary dependencies with:
   ```
   create virtual environment --> see google for your os or your editor
   open terminal
   pip install -r requirements.txt
   ```

3. **Database Setup**: Adjust database settings and execute migrations to establish the database structure:
   ```
   rename the .env.sample to .env and update your settings
   python manage.py makemigrations 
   python manage.py migrate
   ```

4. **Superuser Creation**: Generate a superuser for Django admin access and user management:
   ```
   python manage.py createsuperuser
   ```

5. **App Seed**: If you like you can seed the database with sample data using the following command:
   ```
   python manage.py seed_businesspartner.py
   python manage.py seed_contacts.py
   python manage.py seed_tasks.py
   ```
6. **Server Launch**: Initiate the development server to start the CRM application on your device:
   ```
   python manage.py runserver
   ```

7. **Application Access**: Visit `http://localhost:8000` in a web browser to explore the CRM application. Log in using the superuser credentials to start.
 
