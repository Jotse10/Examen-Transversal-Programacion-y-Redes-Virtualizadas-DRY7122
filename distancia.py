import os, sys, requests

try:
    with open("apikey.txt") as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    print("✗ No encontré 'apikey.txt'. Crea el archivo con tu clave de GraphHopper.")
    sys.exit(1)

if not API_KEY:
    print("✗ 'apikey.txt' está vacío. Agrega tu clave allí.")
    sys.exit(1)
VEHICULOS = {
    "auto": "car",
    "bicicleta": "bike",
    "peatón": "foot"
}

def geocode(ciudad):
    """Geocodifica con GraphHopper y devuelve (lat, lon, país)."""
    url = "https://graphhopper.com/api/1/geocode"
    params = {"q": ciudad, "key": API_KEY}
    r = requests.get(url, params=params).json()
    hits = r.get("hits")
    if not hits:
        raise ValueError(f"No encontré '{ciudad}'")
    top = hits[0]
    country = top.get("country")
    return top["point"]["lat"], top["point"]["lng"], country

def calcula_ruta(o, d, veh):
    """Calcula distancia (km), tiempo (h) e instrucciones."""
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{o[0]},{o[1]}", f"{d[0]},{d[1]}"],
        "vehicle": veh,
        "locale": "es",
        "key": API_KEY,
        "instructions": True
    }
    resp = requests.get(url, params=params).json()
    path = resp["paths"][0]
    dist_km = path["distance"] / 1000.0
    tiempo_h = path["time"] / 3600000.0
    pasos = [instr["text"] for instr in path["instructions"]][:5]
    return dist_km, tiempo_h, pasos

def main():
    print("===== Ítem 2: Ruta Chile → Argentina (GraphHopper) =====")
    while True:
        origen = input("\nCiudad de Origen (Chile) [o 's' para salir]: ")
        if origen.lower() == "s":
            print("¡Chau!")
            break

        destino = input("Ciudad de Destino (Argentina): ")

        try:
            lat_o, lon_o, pais_o = geocode(origen)
            lat_d, lon_d, pais_d = geocode(destino)
        except ValueError as e:
            print("  ✗", e)
            continue

        if pais_o.lower() != "chile":
            print("  ✗ La ciudad de origen debe estar en Chile.")
            continue
        if pais_d.lower() != "argentina":
            print("  ✗ La ciudad de destino debe estar en Argentina.")
            continue

        medio = input(f"Medio ({'/'.join(VEHICULOS)}): ")
        veh = VEHICULOS.get(medio)
        if not veh:
            print("  ✗ Medio no válido, elijo 'car' por defecto.")
            veh = "car"

        dist_km, horas, pasos = calcula_ruta(
            (lat_o, lon_o), (lat_d, lon_d), veh
        )
        dist_mi = dist_km * 0.621371

        print(f"\n→ Distancia: {dist_km:.1f} km / {dist_mi:.1f} mi")
        print(f"→ Tiempo aprox.: {horas:.1f} h en {medio}")
        print("→ Narrativa (primeros pasos):")
        for i, p in enumerate(pasos, 1):
            print(f"   {i}. {p}")
        print()

if __name__ == "__main__":
    main()
