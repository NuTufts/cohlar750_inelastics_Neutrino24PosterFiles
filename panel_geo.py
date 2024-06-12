import numpy as np

def get_panel_coordinates(panel_dimensions, panel_placement, rotation_matrix=None):
    """
    This function takes the dimensions, placement, and optional rotation matrix of a 3D panel object
    and returns the coordinates of its vertices.

    Args:
        panel_dimensions (np.ndarray): A numpy array of shape (3,) representing the width, height, and depth of the panel.
        panel_placement (np.ndarray): A numpy array of shape (3,) representing the x, y, and z coordinates of the panel's center point.
        rotation_matrix (np.ndarray, optional): A 3x3 numpy array representing the rotation matrix. Defaults to None.

    Returns:
        np.ndarray: A numpy array of shape (8, 3) representing the coordinates of the panel's eight vertices.
    """

    # Get half the dimensions for easier calculation
    half_dimensions = panel_dimensions / 2

    # Create an array of all possible vertex offsets relative to the center point
    vertex_offsets = np.array([
        [-half_dimensions[0], -half_dimensions[1], half_dimensions[2]],
        [-half_dimensions[0], -half_dimensions[1],  half_dimensions[2]],
        [-half_dimensions[0],  half_dimensions[1], -half_dimensions[2]],
        [-half_dimensions[0],  half_dimensions[1],  -half_dimensions[2]],
        [ half_dimensions[0], -half_dimensions[1], half_dimensions[2]],
        [ half_dimensions[0], -half_dimensions[1],  half_dimensions[2]],
        [ half_dimensions[0],  half_dimensions[1], -half_dimensions[2]],
        [ half_dimensions[0],  half_dimensions[1],  -half_dimensions[2]],
    ])
    
    # If rotation matrix is provided, apply rotation to vertex offsets
    if rotation_matrix is not None:
        vertex_offsets = np.dot(vertex_offsets, rotation_matrix.T)

    # Add the vertex offsets to the panel placement to get the final vertex coordinates
    return vertex_offsets + panel_placement



# Define rotation angles (in radians) around X, Y, and Z axes for the additional panel
theta_x = np.radians(0)
theta_y = np.radians(0)
theta_z = np.radians(90)
theta_zz = np.radians(45)
theta_anti_zz = np.radians(-45)
# Rotation matrices for the  panels
rotation_matrix_x = np.array([
    [1, 0, 0],
    [0, np.cos(theta_x), -np.sin(theta_x)],
    [0, np.sin(theta_x), np.cos(theta_x)]
])

rotation_matrix_y = np.array([
    [np.cos(theta_y), 0, np.sin(theta_y)],
    [0, 1, 0],
    [-np.sin(theta_y), 0, np.cos(theta_y)]
])

rotation_matrix_z = np.array([
    [np.cos(theta_z), -np.sin(theta_z), 0],
    [np.sin(theta_z), np.cos(theta_z), 0],
    [0, 0, 1]
])

rotation_matrix_zz = np.array([
    [np.cos(theta_zz), -np.sin(theta_zz), 0],
    [np.sin(theta_zz), np.cos(theta_zz), 0],
    [0, 0, 1]
])

rotation_matrix_anti_zz = np.array([
    [np.cos(theta_anti_zz), -np.sin(theta_anti_zz), 0],
    [np.sin(theta_anti_zz), np.cos(theta_anti_zz), 0],
    [0, 0, 1]
])

# Define the corner panel dimensions and placements
corner_panel_dimensions = np.array([31, 1, 220.3])
corner_panel_placements = [
    np.array([36, 36, 0]),    # CornerPanelPos0
    np.array([-36, 36, 0]),   # CornerPanelPos1
    np.array([36, -36, 0]),   # CornerPanelPos2
    np.array([-36, -36, 0])   # CornerPanelPos3
]

# Define the side panel dimensions and placements
# in centimeters
side_panel_dimensions = np.array([66, 10.0, 219.4])
side_panel_placements = [
    np.array([52.0, 0, 0]),   # SidePanelPos0
    np.array([-52.0, 0, 0]),  # SidePanelPos1
    np.array([0, 52.0, 0]),   # SidePanelPos2
    np.array([0, -52.0, 0])   # SidePanelPos3
]
side_panel_rotz_angle = np.array( [90,90,0,0] )

# Apply rotation to get vertex coordinates for each panel
vertex_coordinates_combined_0 = get_panel_coordinates(side_panel_dimensions, side_panel_placements[0],rotation_matrix_z)
vertex_coordinates_combined_1 = get_panel_coordinates(side_panel_dimensions, side_panel_placements[1],rotation_matrix_z)
vertex_coordinates_combined_2 = get_panel_coordinates(side_panel_dimensions, side_panel_placements[2]) #trace 2
vertex_coordinates_combined_3 = get_panel_coordinates(side_panel_dimensions, side_panel_placements[3]) #trace 3

# Apply rotation to get vertex coordinates for each corner panel
corner_vertex_coordinates_combined_0 = get_panel_coordinates(corner_panel_dimensions, corner_panel_placements[0],rotation_matrix_anti_zz)
corner_vertex_coordinates_combined_1 = get_panel_coordinates(corner_panel_dimensions, corner_panel_placements[1],rotation_matrix_zz)
corner_vertex_coordinates_combined_2 = get_panel_coordinates(corner_panel_dimensions, corner_panel_placements[2],rotation_matrix_zz)
corner_vertex_coordinates_combined_3 = get_panel_coordinates(corner_panel_dimensions, corner_panel_placements[3],rotation_matrix_anti_zz)

# Define the panel dimensions and placement for the additional panel
additional_panel_dimensions = np.array([114.5, 114.5, 0])
additional_panel_placement = np.array([0, 0, 110.5])

# Combined rotation matrix for the additional panel
combined_rotation_matrix = np.dot(rotation_matrix_y, rotation_matrix_x)

# Get the coordinates of the additional panel's vertices with combined rotation
additional_vertex_coordinates_combined = get_panel_coordinates(additional_panel_dimensions, additional_panel_placement)

# Create traces for side panels
# side_panel_traces = [
#     go.Mesh3d(x=vertex_coordinates_combined_0[:,0], y=vertex_coordinates_combined_0[:,1], z=vertex_coordinates_combined_0[:,2], color='blue', opacity=0.3),
#     go.Mesh3d(x=vertex_coordinates_combined_1[:,0], y=vertex_coordinates_combined_1[:,1], z=vertex_coordinates_combined_1[:,2], color='blue', opacity=0.3),
#     go.Mesh3d(x=vertex_coordinates_combined_2[:,0], y=vertex_coordinates_combined_2[:,1], z=vertex_coordinates_combined_2[:,2], color='blue', opacity=0.3),
#     go.Mesh3d(x=vertex_coordinates_combined_3[:,0], y=vertex_coordinates_combined_3[:,1], z=vertex_coordinates_combined_3[:,2], color='blue', opacity=0.3)
# ]

# # Create traces for corner panels
# corner_panel_traces = [
#     go.Mesh3d(x=corner_vertex_coordinates_combined_0[:,0], y=corner_vertex_coordinates_combined_0[:,1], z=corner_vertex_coordinates_combined_0[:,2], color='blue', opacity=0.3),
#     go.Mesh3d(x=corner_vertex_coordinates_combined_1[:,0], y=corner_vertex_coordinates_combined_1[:,1], z=corner_vertex_coordinates_combined_1[:,2], color='blue', opacity=0.3),
#     go.Mesh3d(x=corner_vertex_coordinates_combined_2[:,0], y=corner_vertex_coordinates_combined_2[:,1], z=corner_vertex_coordinates_combined_2[:,2], color='blue', opacity=0.3),
#     go.Mesh3d(x=corner_vertex_coordinates_combined_3[:,0], y=corner_vertex_coordinates_combined_3[:,1], z=corner_vertex_coordinates_combined_3[:,2], color='blue', opacity=0.3)
# ]

# # Create traces for the additional panel
# additional_panel_trace = go.Mesh3d(x=additional_vertex_coordinates_combined[:,0], y=additional_vertex_coordinates_combined[:,1], z=additional_vertex_coordinates_combined[:,2], color='blue', opacity=0.3)

