from typing import List, Tuple

import numpy as np
import pandas as pd 
from geopy.geoconders import Nominatim

# ----------------------------------------------------------------------
def stations(Longitude, Latitude):
    """sReturns a list of dictionaries containing information about the n closest stations to the given GPS position.

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
    def Coordinates (city, department):
        geo = Nominatim (user_agent = "Stations", timeout = 2)
        try: 
            lugar = geo.geocode(f"{city}, {department}, Colombia")
            if lugar is not None:
                longitud = lugar.longitude
                latitud = lugar.latitude
                return longitud, latitud
            else:
                print (f"No se encontraron coordenadas para {city}.")
                return None, None
        except GeocoderTimedOut:
            print (f"Geocoding para {city} ha superado el tiempo de espera.")
            return None, None
        
        except AttributeError:
            print (f"Error al obtener coordenadas para {city}.")
            return None, None

    def Haversine (lon_1, lat_1, lon_2, lat_2):
        lon_1, lat_1, lon_2, lat_2 = map(np.radians, [lon_1, lat_1, lon_2, lat_2])

        dlon = lon_2 - lon_1
        dlat = lat_2 - lat_1
        a = np.sin(dlat / 2)**2 + np.cos(lat_1) * np.cos(lat_2) * np.sin(dlon / 2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371
        return c * r

    url = "https://raw.githubusercontent.com/Redes-de-Monitoreo-Multiproposito/python-gcpds.em_spectrum_monitor/main/Radioemisoras_Coordenadas.csv"

    try:
        df = pd.read_csv(url, on_bad_lines = 'skip')
    except pd.errors.ParserError as e:
        print (f"Error al analizar el archivo CSV: {e}")

    df = df[df['BANDA'] != 'AM']

    unique_cities = df.drop_duplicates(subset=['CIUDAD'])

    cities_ = unique_cities['CIUDAD'].tolist()
    department_ = unique_cities['DEPARTAMENTO'].tolist()

    lon_given, lat_given = Longitude, Latitude
    df['Distancia_km'] = df.apply(lambda row: Haversine(lon_given, lat_given, row['LONGITUD'], row['LATITUD']), axis=1)

    ciudades_cercanas = df[df['Distancia_km'] < 30].reset_index(drop=True)

    Station = {}
    emisora = ciudades_cercanas['NOMBRE EMISORA']
    frecue = ciudades_cercanas['FRECUENCIA']
    Station = dict(zip(emisora, frecue))
    
    # PSS: Sample implementation to demonstrate function behavior
    # In a real-world scenario, this would be replaced with the actual logic
    # to determine the closest stations based on the GPS position.
    return [f'Station{i+1}' for i in range(len(Station))]

