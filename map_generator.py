import fastf1
import numpy as np

fastf1.Cache.enable_cache('./cache')

events = fastf1.get_event_schedule(2024, include_testing=False)


def save_coords_to_svg(coords: np.ndarray, filename: str, max_size: int = 1000, stroke_width: int = 2):
    if coords.ndim != 2 or coords.shape[1] != 2:
        raise ValueError("coords must be a numpy array of shape (n_points, 2)")

    x = coords[:, 0]
    y = coords[:, 1]

    # Bounds and dimensions
    min_x, max_x = x.min(), x.max()
    min_y, max_y = y.min(), y.max()
    width = max_x - min_x
    height = max_y - min_y

    # Add padding for stroke width (half on each side)
    padding = stroke_width / 2

    # Scale to fit within max_size including padding
    if width > height:
        scale = (max_size - 2 * padding) / width if width != 0 else 1.0
        svg_width = max_size
        svg_height = height * scale + 2 * padding
    else:
        scale = (max_size - 2 * padding) / height if height != 0 else 1.0
        svg_height = max_size
        svg_width = width * scale + 2 * padding

    # Transform coordinates
    scaled_x = (x - min_x) * scale + padding
    scaled_y = (y - min_y) * scale + padding
    scaled_y = svg_height - scaled_y  # Flip y-axis

    # Build path with closed shape
    path_data = "M " + " L ".join(f"{x_:.2f} {y_:.2f}" for x_, y_ in zip(scaled_x, scaled_y)) + " Z"

    # SVG content
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width:.2f}" height="{svg_height:.2f}" viewBox="0 0 {svg_width:.2f} {svg_height:.2f}">
  <path d="{path_data}" fill="none" stroke="black" stroke-width="{stroke_width}"/>
</svg>
'''

    with open(filename, 'w') as f:
        f.write(svg_content)


def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)


for i in range(len(events)):
    event = events.get_event_by_round(i + 1)
    track_name = str(event['Location']).lower().replace(" ", "-")

    session = event.get_qualifying()

    session.load()

    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()

    circuit_info = session.get_circuit_info()

    # Get an array of shape [n, 2] where n is the number of points and the second
    # axis is x and y.
    track = pos.loc[:, ('X', 'Y')].to_numpy()

    # Convert the rotation angle from degrees to radian.
    track_angle = circuit_info.rotation / 180 * np.pi

    # Rotate and plot the track map.
    rotated_track = rotate(track, angle=track_angle)

    save_coords_to_svg(rotated_track, "tracks/" + track_name + ".svg", 1000, 15)

