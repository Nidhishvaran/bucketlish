from django.shortcuts import render, redirect
import sqlite3

# Create your views here.
def main(request):
    return render(request, 'index.html')

def complete_task(request, task_id):
    if request.method == "POST":
        conn = sqlite3.connect('db.sqlite3', timeout=10)
        crsr = conn.cursor()
        
        # Fetch username from session
        username = request.session.get('username', None)
        
        if username:
            # Update the task status based on the task_id
            crsr.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
            crsr.execute("SELECT * FROM tasks WHERE username = ? AND status = 'Pending'", (username,))

            pending = crsr.fetchall()
            conn.commit()
        else:
            pending = []
        
        crsr.close()
        conn.close()

        # Redirect back to the to-do page or render the template again
        return render(request, 'todo.html', {'tasks': pending})
    
def clear_tasks(request):
    if request.method == "POST":
        conn = sqlite3.connect('db.sqlite3', timeout=10)
        crsr = conn.cursor()
        
        # Fetch username from session
        username = request.session.get('username', None)
        
        if username:
            # Clear all tasks
            crsr.execute("DELETE FROM tasks WHERE username = ?", (username,))
            conn.commit()
        
        crsr.close()
        conn.close()
    return render(request, 'todo.html', {'tasks': []})  # Adjust as necessary to show the updated list

def registration(request):
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")
        
        conn = sqlite3.connect('db.sqlite3', timeout=10)
        crsr = conn.cursor()
        
        # Use parameterized query to prevent SQL injection
        crsr.execute("SELECT * FROM users WHERE username = ?", (name,))
        
        # Fetch the results
        result = crsr.fetchone()
        show_alert = False
        
        if result:
            crsr.execute("SELECT * FROM users WHERE username = ? AND password = ?", (name, password))
            res_ = crsr.fetchone()
            if res_:
                request.session['username'] = name  # Use session to store the username
                crsr.execute("SELECT * FROM tasks WHERE username = ? AND status = 'Pending'", (name,))
                res = crsr.fetchall()
                conn.close()
                print("You've logged in")

                return render(request, 'todo.html', {'tasks': res})
            else:
                show_alert = True
                conn.close()
                print("Incorrect password")

                return render(request, 'index.html', {'show_alert': show_alert})
        else:
            print('User registered successfully!')
            crsr.execute("INSERT INTO users (username, password) VALUES (?, ?)", (name, password))
        
        conn.commit()
        conn.close()
        return render(request, 'index.html')
def add(request):
    if request.method == "POST":
        task = request.POST.get('task_name')

        if task!="":

            # Fetch username from session
            name = request.session.get('username', None)

            if name:
                conn = sqlite3.connect('db.sqlite3', timeout=10)
                crsr = conn.cursor()

                # Check if the task already exists for the user
                check_query = "SELECT * FROM tasks WHERE username = ? AND task_name = ? AND status = 'Pending'"
                crsr.execute(check_query, (name, task))
                existing_task = crsr.fetchone()

                if existing_task is None:  # If no existing task found, insert the new task
                    query = "INSERT INTO tasks (username, task_name, status) VALUES (?, ?, 'Pending')"
                    crsr.execute(query, (name, task))
                    conn.commit()  # Commit after inserting

                # Fetch the updated task list for the user
                crsr.execute("SELECT * FROM tasks WHERE username = ? AND status = 'Pending'", (name,))
                res = crsr.fetchall()

                crsr.close()
                conn.close()

                return render(request, 'todo.html', {'tasks': res})

    return redirect('main')  # Redirect to main page if the method is not POST

# def add(request):
#     if request.method == "POST":
#         task = request.POST.get('task_name')
        
#         # Fetch username from session
#         name = request.session.get('username', None)
        
#         if name:
#             conn = sqlite3.connect('db.sqlite3', timeout=10)
#             crsr = conn.cursor()
            
#             # Insert the new task for the user
#             query = "INSERT INTO tasks (username, task_name, status) VALUES (?, ?, 'Pending')"
#             crsr.execute(query, (name, task))
            
#             crsr.execute("SELECT * FROM tasks WHERE username = ? AND status = 'Pending'", (name,))
#             res = crsr.fetchall()
#             print(res)
            
            
#             crsr.close()
#             conn.commit()
#             conn.close()

#             return render(request, 'todo.html', {'tasks': res})

#     return redirect('main')  # Redirect to main page if the method is not POST
