import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, bending_moment, bending_reinforcement, shear_reinforcement

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure Library to use SQLite database
db = SQL("sqlite:///structural.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure password and confirmation password match
        elif not check_password_hash(
            generate_password_hash(request.form.get("confirmation")),
            request.form.get("password"),):
            return apology("password and confirmation do not match", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not exist already
        if len(rows) != 0 and not check_password_hash(
            rows[0]["username"], request.form.get("username")):
            return apology("username already exists", 400)

        # Add user to database
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)

        return render_template("login.html")
        # Redirect user to home page
        # return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # display a form to register for a new account:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/about")
@login_required
def about():
    """Notes about the programme"""
    return render_template("about.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Index page - select calculation to be performed"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("calculation-selection"):
            return apology("Please select an option", 400)

        n = request.form.get("calculation-selection")

        if n == 'RC-beam':
            return redirect("/RC-beam-0")

        elif n == "Steel-beam":
            return redirect("/Steel-beam-0")

        elif n == "Steel-column":
            return redirect("/Steel-column-0")

        elif n == "Retaining-wall":
            return redirect("/Retaining-wall-0")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # unload all calculation information from the database:
        db.execute("DELETE FROM loads")
        db.execute("DELETE FROM beam_geometry")
        db.execute("DELETE FROM rc_beam_properties")
        # display form for users to select desired calculation:
        return render_template("index.html")

@app.route("/RC-beam-0", methods=["GET", "POST"])
@login_required
def RC_beam():
    """RC_beam - perfrom RC beam calculations - step 1"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        lenght = request.form.get("lenght")
        width = request.form.get("width")
        depth = request.form.get("depth")

        if not lenght:
            return apology("Please review beam geometry information", 400)

        if not width:
            return apology("Please review beam geometry information", 400)

        if not depth:
            return apology("Please review beam geometry information", 400)

        db.execute("INSERT INTO beam_geometry (lenght, width, depth) \
                   VALUES(?, ?, ?)", lenght, width, depth)

        return redirect("/RC-beam-1")
        #return render_template("A_RC-beam-1.html")

    # User reached route via GET (as by submitting a form via GET)
    else:
        return render_template("A_RC-beam-0.html")

@app.route("/RC-beam-1", methods=["GET", "POST"])
@login_required
def RC_beam1():
    """RC_beam - perfrom RC beam calculations - step 2"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("cellA2"):
            return apology("Please provide loading", 400)

        if not request.form.get("cellB2"):
            return apology("Please review loading", 400)

        if not request.form.get("cellC2"):
            return apology("Please review loading", 400)

        if not request.form.get("cellD2"):
            return apology("Please review loading", 400)

        cellA_base_request = "cellA"
        cellB_base_request = "cellB"
        cellC_base_request = "cellC"
        cellD_base_request = "cellD"

    # Loop through all loads and add them to the database:
        cell_no = request.form.get("totalRows")
        i_cell_no = int(cell_no)
        i_cell_no +=1

        for i in range (2, i_cell_no):
            s = str(i)
            cellA_var_request = s
            cellB_var_request = s
            cellC_var_request = s
            cellD_var_request = s

            cellA_request = cellA_base_request + cellA_var_request
            cellB_request = cellB_base_request + cellB_var_request
            cellC_request = cellC_base_request + cellC_var_request
            cellD_request = cellD_base_request + cellD_var_request

            cellA = request.form.get(cellA_request)
            cellB = request.form.get(cellB_request)
            cellC = request.form.get(cellC_request)
            cellD = request.form.get(cellD_request)

            if not cellA:
                return apology("Please review loading table", 400)

            if not cellB:
                return apology("Please review loading table", 400)

            if not cellC:
                return apology("Please review loading table", 400)

            if not cellD:
                return apology("Please review loading table", 400)

            db.execute("INSERT INTO loads (load_type, udl_or_point, load_value, load_position) \
                   VALUES(?, ?, ?, ?)", cellA, cellB, cellC, cellD)

        return redirect("/RC-beam-2")
        #return render_template("A_RC-beam-2.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("A_RC-beam-1.html")

@app.route("/RC-beam-2", methods=["GET", "POST"])
@login_required
def RC_beam2():
    """RC_beam - perfrom RC beam calculations"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        conc_class = request.form.get("concrete")
        rc_density = request.form.get("RCdensity")
        fyk = request.form.get("fyk")
        top_cover = request.form.get("topC")
        bot_cover = request.form.get("bottomC")
        side_cover = request.form.get("sideC")

        if not conc_class:
            return apology("Please review beam properties information", 400)

        if not rc_density:
            return apology("Please review beam properties information", 400)

        if not fyk:
            return apology("Please review beam properties information", 400)

        if not top_cover:
            return apology("Please review beam properties information", 400)

        if not bot_cover:
            return apology("Please review beam properties information", 400)

        if not side_cover:
            return apology("Please review beam properties information", 400)

        db.execute("INSERT INTO rc_beam_properties (conc_class, rc_density, fyk, top_cover, bot_cover, side_cover) \
                   VALUES(?, ?, ?, ?, ?, ?)", conc_class, rc_density, fyk, top_cover, bot_cover, side_cover)

        designProperties = db.execute("SELECT * FROM rc_beam_properties")
        return redirect("/RC-beam-3")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Query database
        table = db.execute("SELECT * FROM concrete_class")
        return render_template("A_RC-beam-2.html", tables=table)

@app.route("/RC-beam-3", methods=["GET", "POST"])
@login_required
def RC_beam3():
    """RC_beam - perfrom RC beam calculations"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        return apology("To Do POST RC beam", 400)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Query database

        #get beam geometry:
        rcBeamGeometry = db.execute("SELECT * FROM beam_geometry")
        length_of_beam = db.execute("SELECT lenght FROM beam_geometry")[0]['lenght']
        width_of_beam = db.execute("SELECT width FROM beam_geometry")
        depth_of_beam = db.execute("SELECT depth FROM beam_geometry")
        #get beam loads:
        beamLoads = db.execute("SELECT * FROM loads")
        point_loads = []
        distributed_loads = []
        # length: Length of the beam
        # point_loads: List of tuples (position, magnitude) for point loads
        # distributed_loads: List of tuples (start_position, end_position, intensity) for distributed loads
        for load in beamLoads:
            if load['udl_or_point'] == "udl":
                load_type = load['load_type']
                intensity = load['load_value']
                # apply load factors here:
                if load_type == "variable":
                    intensity = 1.5 * intensity #apply a factor of 1.5 (maybe change the function in helpers later in order to use factors there instead of here)
                elif load_type == "permanent":
                    intensity = 1.35 * intensity #apply a factor of 1.35 (maybe change the function in helpers later in order to use factors there instead of here)
                starting_point = 0
                end_point = length_of_beam
                load_tuple = (starting_point, end_point, intensity)
                distributed_loads.append(load_tuple)

            if load['udl_or_point'] == "point":
                load_type = load['load_type']
                intensity = load['load_value']
                # apply load factors here:
                if load_type == "variable":
                    intensity = 1.5 * intensity #apply a factor of 1.5 (maybe change the function in helpers later in order to use factors there instead of here)
                elif load_type == "permanent":
                    intensity = 1.35 * intensity #apply a factor of 1.35 (maybe change the function in helpers later in order to use factors there instead of here)
                starting_point = load['load_position']
                load_tuple = (starting_point, intensity)
                point_loads.append(load_tuple)

        static_calculations = bending_moment(length_of_beam, point_loads, distributed_loads)
        rcBeamProperties = db.execute("SELECT * FROM rc_beam_properties")
        tension_reinforcement = bending_reinforcement(rcBeamGeometry, rcBeamProperties, static_calculations)
        shear_rebar = shear_reinforcement(rcBeamGeometry, rcBeamProperties, static_calculations)
        bars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        diameters = [8, 10, 12, 16, 20, 25, 32, 40]

        shear_legs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        shear_spacings = [50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]
        shear_diameters = [8, 10, 12, 16]

        #geometry, material and load properties to be sent to template:
        #geometry
        width = rcBeamGeometry[0]['width']
        depth = rcBeamGeometry[0]['depth']
        length = length_of_beam

        bottom_cover = rcBeamProperties[0]['bot_cover']
        top_cover = rcBeamProperties[0]['top_cover']
        side_cover = rcBeamProperties[0]['side_cover']
        #material
        concrete_class = rcBeamProperties[0]['conc_class']
        f_y = rcBeamProperties[0]['fyk']

        #load - unfactored
        point_loads_unfactored = []
        distributed_loads_unfactored = []
        for load in beamLoads:
            if load['udl_or_point'] == "udl":
                load_type = load['load_type']
                intensity = load['load_value']
                if load_type == "variable":
                    intensity = intensity
                elif load_type == "permanent":
                    intensity = intensity
                starting_point = 0
                end_point = length_of_beam
                load_tuple = (starting_point, end_point, intensity)
                distributed_loads_unfactored.append(load_tuple)

            if load['udl_or_point'] == "point":
                load_type = load['load_type']
                intensity = load['load_value']
                if load_type == "variable":
                    intensity = intensity
                elif load_type == "permanent":
                    intensity = intensity
                starting_point = load['load_position']
                load_tuple = (starting_point, intensity)
                point_loads_unfactored.append(load_tuple)

        return render_template("A_RC-beam-3.html", static_calculations=static_calculations, tension_reinforcement=tension_reinforcement, shear_reinforcement=shear_rebar, bars=bars, diameters=diameters, shear_legs=shear_legs, shear_spacings=shear_spacings, shear_diameters=shear_diameters, length=length, width=width, depth=depth, bottom_cover=bottom_cover, top_cover=top_cover, side_cover=side_cover, concrete_class=concrete_class, f_y=f_y, point_loads=point_loads_unfactored, distributed_loads=distributed_loads_unfactored)

@app.route("/Steel-beam-0", methods=["GET", "POST"])
@login_required
def Steel_beam():
    """RC_beam - perfrom RC beam calculations"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        return apology("To Do POST steel beam", 400)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return apology("To Do GET steel beam", 400)

@app.route("/Steel-column-0", methods=["GET", "POST"])
@login_required
def Steel_column():
    """RC_beam - perfrom RC beam calculations"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        return apology("To Do POST steel column", 400)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return apology("To Do GET steel column", 400)

@app.route("/Retaining-wall-0", methods=["GET", "POST"])
@login_required
def Retaining_wall():
    """RC_beam - perfrom RC beam calculations"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        return apology("To Do POST Ret wall", 400)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return apology("To Do GET Ret wall", 400)
