from typing import List, Tuple


# ----------------------------------------------------------------------
def stations(gps_position: Tuple[int, int, int], n: int = 10) -> List[Dict[str, str]]:
    """Returns a list of dictionaries containing information about the n closest stations to the given GPS position.

    Parameters
    ----------
    gps_position : tuple of int
        A tuple containing the latitude, longitude, and altitude of the GPS position.
    n : int, optional
        The number of closest stations to return (default is 10).

    Returns
    -------
    list of dict
        A list of dictionaries, each containing the 'name' and 'frequency' of the n closest stations.

    Examples
    --------
    >>> stations((40, -74, 0), 5)
    [{'name': 'Station1', 'frequency': '101.1 Hz'},
     {'name': 'Station2', 'frequency': '102.2 Hz'},
     {'name': 'Station3', 'frequency': '103.3 Hz'},
     {'name': 'Station4', 'frequency': '104.4 Hz'},
     {'name': 'Station5', 'frequency': '105.5 Hz'}]
    """

    # PSS: Sample implementation to demonstrate function behavior
    # In a real-world scenario, this would be replaced with the actual logic
    # to determine the closest stations based on the GPS position.
    return [f'Station{i+1}' for i in range(n)]

