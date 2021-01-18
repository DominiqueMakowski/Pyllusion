import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_line, image_rectangle
from ..image.utilities import _coord_line
from ..psychopy import psychopy_line, psychopy_rectangle


def poggendorff_psychopy(window, parameters=None, **kwargs):
    """
    Examples
    ---------    
    >>> import pyllusion as ill
    >>> from psychopy import visual, event
    
    >>> parameters = ill.poggendorff_parameters(difference=0, illusion_strength=-50)
    
    >>> # Initiate Window
    >>> window = visual.Window(size=[800, 600], fullscr=False,
                               screen=0, winType='pygame', monitor='testMonitor',
                               allowGUI=False, color="white",
                               blendMode='avg', units='pix')
    
    >>> # Display illusion
    >>> ill.poggendorff_psychopy(window=window, parameters=parameters)

    >>> # Refresh and close window    
    >>> window.flip()
    >>> event.waitKeys()  # Press any key to close
    >>> window.close()
    """
    
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = poggendorff_parameters(**kwargs)

    # Draw lines
    for pos in ["Left_", "Right_"]:
        psychopy_line(window,
                      x1=parameters[pos + "x1"],
                      y1=parameters[pos + "y1"],
                      x2=parameters[pos + "x2"],
                      y2=parameters[pos + "y2"],
                      adjust_height=True, color="red", size=5)
    
    # Draw shaded rectangle
    psychopy_rectangle(window, x=0, y=parameters["Rectangle_y"],
                       size_width=parameters["Rectangle_Width"],
                       size_height=parameters["Rectangle_Height"], color="grey",
                       outline_color="grey")


def poggendorff_image(
    parameters=None, width=800, height=600, background="white", **kwargs
):
    """Create the Poggendorff illusion.
    The Poggendorff illusion is an optical illusion that involves the misperception
    of the position of one segment of a transverse line that has been interrupted
    by the contour of an intervening structure.

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.poggendorff_parameters(difference=0, illusion_strength=-55)
    >>> ill.poggendorff_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>


    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = poggendorff_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Lines
    for pos in ["Left_", "Right_"]:
        image = image_line(
            image=image,
            x1=parameters[pos + "x1"],
            y1=parameters[pos + "y1"],
            x2=parameters[pos + "x2"],
            y2=parameters[pos + "y2"],
            color="red",
            adjust_height=True,
            size=20,
        )

    image = image_rectangle(
        image=image,
        y=parameters["Rectangle_y"],
        size_width=parameters["Rectangle_Width"],
        size_height=parameters["Rectangle_Height"],
        color="grey",
        adjust_height=False,
        size=20,
    )

    return image


def poggendorff_parameters(difference=0, illusion_strength=0):
    """
    Zollner Illusion

    Parameters
    ----------
    difficulty : float
        Top line angle (clockwise).
    illusion : float
        Top distractor lines angle (clockwise).
    """
    y_offset = difference

    # Coordinates of left line
    angle = 90 - illusion_strength
    angle = angle if illusion_strength >= 0 else -angle
    coord, _, _ = _coord_line(x1=0, y1=0, angle=-angle, length=0.75)
    left_x1, left_y1, left_x2, left_y2 = coord

    # Right line
    coord, _, _ = _coord_line(x1=0, y1=y_offset, angle=180 - angle, length=0.75)
    right_x1, right_y1, right_x2, right_y2 = coord

    parameters = {
        "Illusion": "Poggendorff",
        "Illusion_Strength": illusion_strength,
        "Difference": difference,
        "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
        "Left_x1": left_x1,
        "Left_y1": left_y1,
        "Left_x2": left_x2,
        "Left_y2": left_y2,
        "Right_x1": right_x1,
        "Right_y1": right_y1,
        "Right_x2": right_x2,
        "Right_y2": right_y2,
        "Angle": angle,
        "Rectangle_Height": 1.75,
        "Rectangle_Width": 0.5,
        "Rectangle_y": 0,
    }

    return parameters
