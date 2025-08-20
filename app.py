from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Initialize Firebase Admin with your service account JSON file and database URL
cred = credentials.Certificate('nidsticket01-firebase.json')  # replace with your file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nidsticket01-default-rtdb.asia-southeast1.firebasedatabase.app/'  # replace with your Firebase Realtime DB URL
})

@app.route("/")
def home():
    return render_template('home.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')  # Your provided HTML form saved as templates/register.html

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle form data here
        data = {
            'id_no': request.form.get('id_no'),
            'name': request.form.get('name'),
            'address': request.form.get('address'),
            'gs_division': request.form.get('gs_division'),
            'mobile_no': request.form.get('mobile_no'),
            'marital_status': request.form.get('marital_status'),
            'occupation': request.form.get('occupation'),
            'family_members': request.form.get('family_members')
        }
        # Reference to Firebase Realtime Database under 'registrations' node
        ref = db.reference('dsclients')
        
        # Push the data to the database with a unique key
        ref.push(data)
        # process data, save to db, etc.
        print('Form submitted!')
        # Redirecting or rendering the same template is okay,
        # but redirect after POST is better to prevent resubmission
        return redirect(url_for('register'))
    return render_template('register.html')



# @app.route('/submit-registration', methods=['POST'])
# def submit_registration():
#     # Extract form data
#     data = {
#         'id_no': request.form.get('id_no'),
#         'name': request.form.get('name'),
#         'address': request.form.get('address'),
#         'gs_division': request.form.get('gs_division'),
#         'mobile_no': request.form.get('mobile_no'),
#         'marital_status': request.form.get('marital_status'),
#         'occupation': request.form.get('occupation'),
#         'family_members': request.form.get('family_members')
#     }

#     # Reference to Firebase Realtime Database under 'registrations' node
#     ref = db.reference('registrations')
    
#     # Push the data to the database with a unique key
#     ref.push(data)

#     return redirect(url_for('register_success'))

@app.route('/register-success')
def register_success():
    return "<h2>Registration Successful!</h2><a href='/register'>Back to Registration</a>"

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
