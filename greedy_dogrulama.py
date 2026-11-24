from collections import defaultdict
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

nufuslar = {
    int(f["fid"]): int(f["nufus"])
    for f in talep.getFeatures()
}

aday_kapsama = defaultdict(set)

for f in od.getFeatures():
    if float(f["total_cost"]) <= 400:
        aday_id = int(f["destination_id"])
        talep_id = int(f["origin_id"])
        aday_kapsama[aday_id].add(talep_id)

kapsanan = set()
secimler = []

for sira in range(1, 11):
    en_iyi_aday = None
    en_iyi_nufus = 0
    en_iyi_talepler = set()

    for aday_id, talepler in aday_kapsama.items():
        if aday_id in secimler:
            continue

        yeni_talepler = talepler - kapsanan
        kazanilan = sum(nufuslar[t] for t in yeni_talepler)

        if kazanilan > en_iyi_nufus:
            en_iyi_aday = aday_id
            en_iyi_nufus = kazanilan
            en_iyi_talepler = yeni_talepler

    if en_iyi_aday is None:
        break

    secimler.append(en_iyi_aday)
    kapsanan.update(en_iyi_talepler)

    print(
        sira,
        "Aday:", en_iyi_aday,
        "Yeni kapsanan nüfus:", en_iyi_nufus
    )

toplam_nufus = sum(nufuslar.values())
kapsanan_nufus = sum(nufuslar[t] for t in kapsanan)

print("\nSEÇİLEN ADAYLAR:", secimler)
print("Seçilen aday sayısı:", len(secimler))
print("Kapsanan talep noktası:", len(kapsanan))
print("Kapsanan nüfus:", kapsanan_nufus)
print("Toplam talep nüfusu:", toplam_nufus)
print(
    "Kapsama oranı (%):",
    round(100 * kapsanan_nufus / toplam_nufus, 2)
)