from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsVectorFileWriter,
    QgsWkbTypes
)

p = QgsProject.instance()

aday = next(
    l for l in p.mapLayers().values()
    if l.name() == "mclp_yeni_durak_adaylari_on_secim"
)

secimler = [294, 164, 832, 200, 207, 78, 55, 280, 616, 184]

# Yeni geçici nokta katmanı
geometri = QgsWkbTypes.displayString(aday.wkbType())

yeni = QgsVectorLayer(
    f"{geometri}?crs={aday.crs().authid()}",
    "mclp_10_yeni_durak_secimi_greedy",
    "memory"
)

dp = yeni.dataProvider()
dp.addAttributes(aday.fields())
yeni.updateFields()

# Seçilen 10 adayın geometrilerini ve özniteliklerini kopyala
eklenecek = []

for f in aday.getFeatures():
    if int(f["fid"]) in secimler:
        nf = QgsFeature(yeni.fields())
        nf.setGeometry(f.geometry())
        nf.setAttributes(f.attributes())
        eklenecek.append(nf)

dp.addFeatures(eklenecek)
yeni.updateExtents()

# GeoPackage'a kaydet
dosya = r"D:\opengis\proje\Esenyurt_Ulasim_Optimizasyonu.gpkg"

options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "GPKG"
options.layerName = "mclp_10_yeni_durak_secimi_greedy"
options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer

sonuc = QgsVectorFileWriter.writeAsVectorFormatV3(
    yeni,
    dosya,
    p.transformContext(),
    options
)

print("Kaydetme sonucu:", sonuc)
print("Kaydedilen durak sayısı:", len(eklenecek))

if sonuc[0] == QgsVectorFileWriter.NoError and len(eklenecek) == 10:
    kayitli = QgsVectorLayer(
        dosya + "|layername=mclp_10_yeni_durak_secimi_greedy",
        "mclp_10_yeni_durak_secimi_greedy",
        "ogr"
    )

    if kayitli.isValid():
        p.addMapLayer(kayitli)
        print("Katman başarıyla eklendi.")
        print("Katman kayıt sayısı:", kayitli.featureCount())