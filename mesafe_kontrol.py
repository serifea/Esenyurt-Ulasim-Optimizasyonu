
from qgis.core import QgsProject

p = QgsProject.instance()

od = next(
    l for l in p.mapLayers().values()
    if "mclp_talep_aday_durak_yuru" in l.name()
)

mesafeler = [
    float(f["total_cost"])
    for f in od.getFeatures()
]

uygun = [
    f for f in od.getFeatures()
    if float(f["total_cost"]) <= 400
]

print("TOPLAM OD KAYDI:", len(mesafeler))
print("EN KISA MESAFE:", min(mesafeler))
print("EN UZUN MESAFE:", max(mesafeler))
print("400 METRE ICINDEKI ESLESME:", len(uygun))

print(
    "400 METRE ICINDEKI FARKLI TALEP:",
    len(set(int(f["origin_id"]) for f in uygun))
)

print(
    "400 METRE ICINDEKI FARKLI ADAY:",
    len(set(int(f["destination_id"]) for f in uygun))
)

print("\n400 METRE ICINDEKI ILK 20 KAYIT:")

for i, f in enumerate(uygun):
    if i == 20:
        break

    print(
        "Origin:", f["origin_id"],
        "Destination:", f["destination_id"],
        "Mesafe:", f["total_cost"]
    )
