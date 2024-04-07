## Initial Setup

For local deployment, follow these instructions:

1. **Repository Cloning**: Use the command below to clone the app repository to your machine:
   ```
   git clone https://github.com/dmm1/Ecosphere.git
   ```

2. **Dependency Installation**: Within the project folder, install necessary dependencies with:
   ```
   pip install -r requirements.txt
   ```

3. **Database Setup**: Adjust database settings and execute migrations to establish the database structure:
   ```
   Edit the settings.py file to your database settings.
   python main.py makemigrations ecosphere
   python main.py migrate
   ```

4. **Superuser Creation**: Generate a superuser for Django admin access and user management:
   ```
   python main.py createsuperuser
   ```

5. **Server Launch**: Initiate the development server to start the CRM application on your device:
   ```
   python main.py runserver
   ```

6. **Application Access**: Visit `http://localhost:8000` in a web browser to explore the CRM application. Log in using the superuser credentials to start.
 
