from PIL import Image, ImageSequence


# Helper function to check if a color is a shade of red
def is_red(color):
    r, g, b = color[:3]
    return r > g * 1.5 and r > b * 1.5


# Helper function to transform red to orange
def transform_color(color):
    r, g, b = color[:3]
    # Ensure new values are within the byte range before returning
    new_r = max(min(r, 255), 0)  # Red is set to 0 since we are removing red.
    new_g = max(min(g, 165), 0)  # Green remains the same.
    new_b = max(min(b + r, 0), 0)  # Adding the red value to blue, capped at 255.
    return (new_r, new_g, new_b, 255) if is_red(color) else color


# Open the original GIF
with Image.open("./crunch.gif") as img:
    # Ensure the image is in P mode which contains a palette
    if img.mode != "P":
        img = img.convert("P")

    # Create a list to hold the transformed frames
    transformed_frames = []

    # Iterate over each frame in the animated GIF
    for frame in ImageSequence.Iterator(img):
        # Make sure to convert frames to mode 'P' as well
        frame = frame.convert("P")

        # Load the current frame's palette
        palette = frame.getpalette()

        # Update the palette by transforming red colors to blue
        for i in range(0, len(palette), 3):
            color = tuple(palette[i : i + 3])
            if is_red(color):
                new_color = transform_color(color)
                palette[i : i + 3] = new_color[:3]

        # Assign the updated palette back to the frame
        frame.putpalette(palette)

        # Append the transformed frame to the list
        transformed_frames.append(frame.copy())

    # Save the frames as a new GIF
    transformed_frames[0].save(
        "./crunch-modified.gif",
        save_all=True,
        append_images=transformed_frames[1:],
        loop=0,
        duration=img.info.get(
            "duration", 100
        ),  # Providing a default duration if not present
        disposal=img.info.get("disposal", 2),  # Providing a default disposal method
    )
