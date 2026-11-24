
from qgis.core import QgsProject

p = QgsProject.instance()

talep = next(
    l for l in p.mapLayers().values()
    if l.name() == "mclp_kapsama_disi_talep_noktalari_nokta2"
)

od = next(
    l for l in p.mapLayers().values()
    if "mclp_talep_aday_durak_yuru" in l.name()
)

print("Talep katmani:")

for f in talep.getFeatures():
    print(f["fid"], f["name"], f["nufus"])

print("\nOD katmanindaki ilk 15 eslesme:")

for i, f in enumerate(od.getFeatures()):
    print(
        "Origin:", f["origin_id"],
        "Destination:", f["destination_id"],
        "Mesafe:", f["total_cost"]
    )
    if i == 14:
        break
