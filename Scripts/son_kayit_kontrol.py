from qgis.core import QgsProject, QgsVectorLayer

dosya = r"D:\opengis\proje\Esenyurt_Ulasim_Optimizasyonu.gpkg"

katman = QgsVectorLayer(
    dosya + "|layername=mclp_10_yeni_durak_secimi_greedy",
    "kontrol",
    "ogr"
)

print("Katman geçerli:", katman.isValid())
print("Kayıt sayısı:", katman.featureCount())

print("Seçilen FID değerleri:")

for f in katman.getFeatures():
    print("FID:", f["fid"], "Geometri boş:", f.geometry().isEmpty())