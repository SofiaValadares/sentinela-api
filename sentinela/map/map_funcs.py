import geopandas as gpd
from shapely.geometry import Point

# Caminho para o arquivo baixado
arquivo_geojson = "./sentinela/map/map.geojson"

# Carrega o GeoJSON local
estados = gpd.read_file(arquivo_geojson)

# Estados com presença de Caatinga
estados_caatinga = [
    "ALAGOAS", "BAHIA", "CEARA", "MARANHAO", "PARAIBA",
    "PERNAMBUCO", "PIAUI", "RIO GRANDE DO NORTE", "SERGIPE", "MINAS GERAIS"
]

malha_caatinga = estados[estados["name"].isin(estados_caatinga)]

# Função para encontrar estado de uma coordenada
def find_state(lat, lon):
    ponto = Point(lon, lat)  # Ordem: (lon, lat)
    estado = malha_caatinga[malha_caatinga.contains(ponto)]


    if not estado.empty:
        return estado.iloc[0]["name"]
    return "Coordenada fora da Caatinga"

