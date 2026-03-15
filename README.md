Retention and Analytics App.

I built this to solve a real problem we have at the lab which is, tracking quality assurance and keeping doctors happy. Since our lab runs entirely on paper prescriptions, nobody at the workbenches can use a computer to log data. To fix this, I built an app specifically for the final quality control desk. When a manager catches a remake, they can use a fast, simple form to log the defect and tie it directly to the specific doctor and the department at fault.

For this app i used Python and the Django framework and a simple SQLite database for the incoming tickets. I used faker library to generate the data to use for this in order to test functionality.
On the frontend i used Chart.js to have a visual of where the lab is having issues.
I added AI feature that uses Google Gemini API to actively flag which doctors are at the highest risk of leaving based on their recent remakes. It looks at the specific defect, like a short margin in Crown & Bridge, and generates a custom, practical suggestion for the lab manager on exactly how to save the account and prevent the doctor from going to a competitor.



Setup guide:
To run this on your own machine, clone the repo and create a .env file in the main folder with your GEMINI_API_KEY. Install the requirements by running python -m pip install requirements.txt. Set up the database by running python manage.py makemigrations and python manage.py migrate, then run python manage.py seed_data to fill it with test data. Finally, start the server with python manage.py runserver and follow the link provided in the terminal.



