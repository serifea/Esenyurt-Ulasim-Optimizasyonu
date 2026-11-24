from qgis.core import QgsProject

layers = list(QgsProject.instance().mapLayers().values())

od = next(l for l in layers if "mclp_400m_aday_durak_eslesmeleri" in l.name())
weights_layer = next(l for l in layers if "mclp_mahalle_aday_durak_nufus_birlesik_son" in l.name())
candidates = next(l for l in layers if "mclp_yeni_durak_adaylari_on_secim" in l.name())

print("OD kayıt:", od.featureCount())
print("Nüfus kayıt:", weights_layer.featureCount())
print("Aday kayıt:", candidates.featureCount())

od_ids = {int(f["destination_id"]) for f in od.getFeatures()}
candidate_ids = {int(f["fid"]) for f in candidates.getFeatures()}

print("Eşleşen aday kimliği:", len(od_ids & candidate_ids))
print("Nüfus alanı:", weights_layer.fields().indexFromName("nufus"))
print("Mahalle adı alanı:", weights_layer.fields().indexFromName("name"))