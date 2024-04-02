import contextlib
from pathlib import Path
from typing import Dict, Tuple

from rpapy.core.config import Config
from rpapy.core.snipps.loads import create_python_default_dirs


def map_images():
    """Mapping the images captured by agent.py and saves them in the images directory. 
    Use the name of the image to    retrieve the region where the image should be 
    searched and the displacement of the anchor where the action should be performed.
    
    Returns:
        [dict] -- [dictionary containing the image data]
    """
    create_python_default_dirs()

    # retrieves the directory where the images are stored
    with contextlib.suppress(FileExistsError):
        Config.IMAGES_DIR_PATH.mkdir(parents=True)    

    result: Dict[str, Dict[str, Tuple[int]]] = {}

    # Recovers all image files in name+region or name+region+anchor format.
    images_path = Config.IMAGES_DIR_PATH.glob('*).png')

    # Iterates through all images found in the directory
    # Retrieves the name and the tuple that indicates the region of the image
    # Adds the data to a literal dict and adds it to the result dict using the default method.
    for p in images_path:
        p: Path = p

        anchor_coord = None
        name, *_ = p.name.split('-')
        
        if '#' in p.name:
            remaining, anchor_coord = p.name.removeprefix(name+'-').split('#')
            region_tuple = tuple(int(i) for i in remaining[1:-1].split(','))
            anchor_coord = tuple(int(i) for i in anchor_coord.split('.')[0][1:-1].split(','))

        else:
            remaining = p.name.removeprefix(name+'-')
            region_tuple = tuple(int(i) for i in remaining.removesuffix('.png')[1:-1].split(','))
        
        result.setdefault(name, {
            'image': p.as_posix(), 
            'region': region_tuple, 
            'anchor_coord': anchor_coord,
        })
    return result