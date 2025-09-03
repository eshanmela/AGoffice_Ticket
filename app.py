import firebase_admin, time

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from firebase_admin import credentials, db
from datetime import datetime

app = Flask(__name__)
app.secret_key = "AIzaSyD9HClMIavq24aHR6hmPWGdV5dkx7BgBg8"
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

#Update Ticket class
@app.route('/edit_ticket/<ticket_id>', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    ref = db.reference('tickets').child(ticket_id)

    if request.method == 'POST':
        # Get form data
        visitedreason = request.form.get('visitedreason')
        jobstatus = request.form.get('jobstatus')
        dateandtime = request.form.get('dateandtime')

        update_data = {
            'visitedreason': visitedreason,
            'jobstatus': jobstatus,
            'dateandtime': dateandtime,
        }

        # Update the ticket in Firebase
        try:
            ref.update(update_data)
            flash('Ticket updated successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error updating ticket: {str(e)}', 'danger')

    # For GET request, retrieve the existing ticket data to pre-fill the form
    ticket = ref.get()
    if not ticket:
        flash('Ticket not found.', 'warning')
        return redirect(url_for('home'))

    return render_template('updateTicket.html', ticket_id=ticket_id, ticket=ticket)

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

@app.route('/ticket', methods=['GET'])
def ticket_form():
    return render_template('ticket_form.html')

# Route to handle form submission
@app.route('/ticket', methods=['POST'])
def ticket_submit():
    current_time_iso = datetime.utcnow().isoformat()
    ticket_data = {
        'ticketID': request.form.get('ticketID'),
        'visitedReason': request.form.get('visitedreason'),
        'jobStatus': request.form.get('jobstatus'),
        'dateandtime': current_time_iso
    }


    ref = db.reference('tickets')
    
    # Push the data to the database with a unique key
    ref.push(ticket_data)


    # Here you can save ticket_data to database, Firebase, etc.
    print("Received ticket data:", ticket_data)
    return redirect(url_for('ticket_form')) 

@app.route('/clientview/<ticket_id>', methods=['GET'])
def clientview(ticket_id):
    ref_tickets = db.reference('tickets')
    results_tickets = ref_tickets.order_by_child('ticketID').equal_to(ticket_id).get()

    ref_jobs = db.reference('jobSummery')
    results_jobs = ref_jobs.order_by_child('ticketid').equal_to(ticket_id).get()

    if results_tickets:
        first_ticket = next(iter(results_tickets.values()))
        job_task_list = list(results_jobs.values())  # Convert dict_values to list to pass to template
        return render_template('clientview.html', tickets=first_ticket, jobsummery=job_task_list)
    else:
        return "Ticket not found", 404

# @app.route('/clientview/<ticket_id>', methods=['GET'])
# def clientview(ticket_id):
#     ref_tickets = db.reference('tickets')
#     # Query tickets where child 'ticketID' equals the given ticket_id
#     results_tickets = ref_tickets.order_by_child('ticketID').equal_to(ticket_id).get()

#     ref_jobs = db.reference('jobSummery')
#     results_jobs = ref_jobs.order_by_child('ticketid').equal_to(ticket_id).get()

#     if results_tickets:
#         # results is a dict; return first matching ticket
#         first_ticket = next(iter(results_tickets.values()))
#         first_jobtask = next(list(results_jobs.values()))
#         # return jsonify(first_ticket)
#         return render_template('clientview.html', tickets=first_ticket, jobsummery=first_jobtask)
#     else:
#         return jsonify({'error': 'Ticket not found'}), 404

# def displayjobtasks(ticket_id):
#     ref = db.reference('jobSummery')
#     # Query tickets where child 'ticketID' equals the given ticket_id
#     results = ref.order_by_child('ticketid').equal_to(ticket_id).get()

#     if results:
#         # results is a dict; return first matching ticket
#         jobtasks = next(iter(results.values()))
#         # return jsonify(first_ticket)
#         return render_template('clientview.html', jobstatus=jobtasks)
#     else:
#         return jsonify({'error': 'Ticket not found'}), 404



@app.route('/clientview_redirect')
def clientview_redirect():
    ticket_id = request.args.get('ticketid')
    if ticket_id:
        return redirect(url_for('clientview', ticket_id=ticket_id))
    else:
        return "Ticket ID required", 400
    

@app.route('/ticketview')
def view_tickets():
    ref = db.reference('tickets')  # Your tickets node
    tickets_data = ref.get()

#     # tickets_data is a dict with ticket keys and values
#     # Pass it to template to render
    return render_template('tickets.html', tickets=tickets_data)



@app.route('/filter_tickets')
def filter_tickets():
    ref = db.reference('tickets')  # Your tickets node
    tickets_data = ref.get()

    # tickets_data is a dict with ticket keys and values
    # Pass it to template to render
    return render_template('filterTickets.html', tickets=tickets_data)

@app.route('/ticketbyID')
def ticketsbyID():
    ref = db.reference('tickets')  # Your tickets node
    tickets_data = ref.get()

    # tickets_data is a dict with ticket keys and values
    # Pass it to template to render
    return render_template('ticketStatus.html', tickets=tickets_data)

if __name__ == '__main__':
    app.run(debug=True)
