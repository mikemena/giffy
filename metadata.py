from PIL import Image

# Open the GIF file
with Image.open("./crunch.gif") as img:
    # Access metadata
    metadata = img.info
    print(metadata)

    # If you need to modify or add metadata, it's somewhat limited for GIFs,
    # but you can manipulate what's available in the img.info dictionary.
    # For example, to add a custom metadata field:
    img.info["custom_meta"] = "value"

    # Note: Saving modifications like this might not always be supported for GIFs due to the format's limitations.
