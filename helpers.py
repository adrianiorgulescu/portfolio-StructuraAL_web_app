import re
from statistics import mean

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# FUNCTION FOR PROCESSING LOAD INFO FROM DATABASE:
def process_database_load_info(beamLoads, length_of_beam):
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
                intensity = 1.5 * intensity #apply a factor of 1.5 
            elif load_type == "permanent":
                intensity = 1.35 * intensity #apply a factor of 1.35 
            starting_point = 0
            end_point = length_of_beam
            load_tuple = (starting_point, end_point, intensity)
            distributed_loads.append(load_tuple)

        if load['udl_or_point'] == "point":
            load_type = load['load_type']
            intensity = load['load_value']
            # apply load factors here:
            if load_type == "variable":
                intensity = 1.5 * intensity #apply a factor of 1.5 
            elif load_type == "permanent":
                intensity = 1.35 * intensity #apply a factor of 1.35
            starting_point = load['load_position']
            load_tuple = (starting_point, intensity)
            point_loads.append(load_tuple)

    return(point_loads, distributed_loads)

# FUNCTION FOR PROCESSING LOAD INFO FROM DATABASE (UNFACTORED LOADS FOR TEMPLATE USE):
def process_database_load_info_unfactored(beamLoads, length_of_beam):
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
            
    return(point_loads_unfactored, distributed_loads_unfactored)

# FUNCTION FOR STATIC CALCULATIONS:
def static_calcs(length, point_loads, distributed_loads):

    # Transform distributed loads in equivalent point loads:
    equivalent_point_loads = transform_distributed_to_point(distributed_loads)
    
    # Add the equivalent point loads to the point loads list:
    new_point_loads = point_loads + equivalent_point_loads

    # Calculate reaction forces from the equilibrium equations:
    reaction_A, reaction_B = calculate_reactions(new_point_loads, length)

    # Get maximum bending moment:
    max_bending_moment = get_max_bending_moment(point_loads, distributed_loads, reaction_A, length)
    
    # Get min and max shear force values:
    min_shear_force, max_shear_force = get_shear_forces(point_loads, distributed_loads, reaction_A, length)

    return(round(reaction_A, 1), round(reaction_B,1), round(max_bending_moment,1), round(max_shear_force,1), round(min_shear_force,1))

# FUNCTION FOR DETERMINING BENDING REINFORCEMENT REQUIREMENT
def bending_reinforcement(beam_geometry, beam_properties, static_calculations):
    """
    Calculate the bending reinforcement requirement for a rectangular sections (only tension reinforcement considered).

    Parameters:
    - beam_geometry
    - beam_properties
    - static_calculations

    From which the following will be obtained:
        b: Width of the beam (in mm)
        d: Effective depth of the beam (in mm)
        f_c: Characteristic strength of concrete (in MPa)
        f_y: Yield strength of reinforcement (in MPa)
        M: Bending moment (in kNm)
        bottom_cover: bottom rebar cover (in mm)

    Returns:
    - required area of reinforcement (in sqmm)
    """

    #retrieve the design variables:
    d = beam_geometry[0]['depth']
    concrete_class = beam_properties[0]['conc_class']
    f_c = re.split("[/]", concrete_class)[0]
    f_c = re.split("[C]", f_c)[1]
    f_y = beam_properties[0]['fyk']
    bottom_cover = beam_properties[0]['bot_cover']
    M = static_calculations[2]

    # Constants
    gamma_s = 1.15  # Partial safety factor for steel

    # Convert units
    M_d = M * 1e6  # Convert kNm to Nmm

    # Calculate lever arm 'a' (distance from the centroid of the compression zone to the extreme fiber)
    d_d = d - bottom_cover - 10 # (considering a 20mm dia bar is provided, which is conservative)
    a = 0.9 * d_d  # Assuming a rectangular stress block and providing a factor of safety
    # Calculate the design steel strength
    f_y_d = float(f_y) / gamma_s

    # Calculate the area of tension reinforcement required and return the value
    A_s_req = round(((M_d) / (f_y_d * a)),1)
    return A_s_req

# FUNCTION FOR DETERMINING SHEAR REINFORCEMENT REQUIREMENT
def shear_reinforcement(beam_geometry, beam_properties, static_calculations):
    """
    Calculate the shear reinforcement requirement for a rectangular sections.

    Parameters:
    - beam_geometry
    - beam_properties
    - static_calculations

    From which the following will be obtained:
        b: Width of the beam (in mm)
        d: Effective depth of the beam (in mm)
        f_c: Characteristic strength of concrete (in MPa)
        f_y: Yield strength of reinforcement (in MPa)
        V: shear force (in kN)
        bottom_cover: bottom rebar cover (in mm)

    Returns:
    - required area of reinforcement (in sqmm / m)
    """

    #retrieve the design variables:
    d = beam_geometry[0]['depth']
    concrete_class = beam_properties[0]['conc_class']
    f_c = re.split("[/]", concrete_class)[0]
    f_c = re.split("[C]", f_c)[1]
    f_y = beam_properties[0]['fyk']
    bottom_cover = beam_properties[0]['bot_cover']
    V = max(abs(static_calculations[3]), abs(static_calculations[4]))

    # Constants
    gamma_s = 1.15  # Partial safety factor for steel

    # Convert units
    V_d = V * 1e3  # Convert kN to N

    # Calculate lever arm 'a' (distance from the centroid of the compression zone to the extreme fiber)
    d_d = d - bottom_cover - 10 # (considering a 20mm dia bar is provided, which is conservative)
    z = 0.9 * d_d  # Assuming a rectangular stress block and providing a factor of safety

    # Calculate the design concrete strength & steel strength
    f_y_d = float(f_y) / gamma_s

    # Calculate As_w (per meter) and return the value
    As_w = round((V_d * 1000 / z / (0.8 * f_y_d) / 1),1)
    return As_w

def transform_distributed_to_point(distributed_loads):
    equivalent_point_loads = []
    for start_position, end_position, load_intensity in distributed_loads:
        mid_point = (start_position + end_position) / 2
        equivalent_point_load = load_intensity * (end_position - start_position)
        load_tuple = (mid_point, equivalent_point_load)
        equivalent_point_loads.append(load_tuple)
    return equivalent_point_loads

# Calculate reaction forces from the equilibrium equations:
def calculate_reactions(new_point_loads, length):
    reaction_A = reaction_B = 0
    point_load_sum = 0
    magnitude_position_pair = 0

    for load_position, load_magnitude in new_point_loads:
        point_load_sum += load_magnitude
        magnitude_position_pair += (load_position * load_magnitude)

    reaction_B = magnitude_position_pair / length
    reaction_A = point_load_sum - reaction_B
    return(reaction_A, reaction_B)

def get_max_bending_moment(point_loads, distributed_loads, reaction_A, length):
    # Calculate bending moments in all beam sections considering an increment of 0.1mm (0.0001m) and get the maximum value:
    bending_moment_list = [] # Initialize the bending moment list for all relevant positions:

    for x in range(int(length)): # x represent the section where we are doing the calculations

        bending_moment_increments = []

        # a) Get the bending moment from the point loads (check only equilibrium on left hand side):
        for load_position, load_magnitude in point_loads:
            if load_position < x:
                bending_moment_i = (-1) * load_magnitude * (x - load_position)
                bending_moment_increments.append(bending_moment_i)

        # a) Get the bending moment from the distributed loads (check only equilibrium on left hand side):
        for start_position, end_position, load_intensity in distributed_loads:
            if start_position < x and end_position < x:
                bending_moment_i = (-1) * load_intensity * (x - ((start_position + end_position)/2)) * (end_position - start_position)
                bending_moment_increments.append(bending_moment_i)

            if start_position < x and end_position >= x:
                bending_moment_i = (-1) * load_intensity * (x - ((start_position + x)/2)) * (x - start_position)
                bending_moment_increments.append(bending_moment_i)

        x += 0.0001

        bending_moment = reaction_A * x + sum(bending_moment_increments)
        bending_moment_list.append(bending_moment)

    max_bending_moment = round(max(bending_moment_list),2)
    return(max_bending_moment)

def get_shear_forces(point_loads, distributed_loads, reaction_A, length):
    # Calculate shear force in all beam sections considering an increment of 0.1mm (0.0001m):
    shear_force_list = [] # Initialize the shear force list for all relevant positions:

    for x in range(int(length)): # x represent the section where we are doing the calculations

        shear_force_increments = []

        # a) Get the shear force from the point loads (check only equilibrium on left hand side):
        for load_position, load_magnitude in point_loads:
            if load_position < x:
                shear_force_i = (-1) * load_magnitude
                shear_force_increments.append(shear_force_i)

        # a) Get the shear force from the distributed loads (check only equilibrium on left hand side):
        for start_position, end_position, load_intensity in distributed_loads:
            if start_position < x and end_position < x:
                shear_force_i = (-1) * load_intensity * (end_position - start_position)
                shear_force_increments.append(shear_force_i)

            if start_position < x and end_position >= x:
                shear_force_i = (-1) * load_intensity * (x - start_position)
                shear_force_increments.append(shear_force_i)

        x += 0.0001

        shear_force = reaction_A + sum(shear_force_increments)
        shear_force_list.append(shear_force)

    max_shear_force = round(max(shear_force_list),2)
    min_shear_force = round(min(shear_force_list),2)

    return(min_shear_force, max_shear_force)