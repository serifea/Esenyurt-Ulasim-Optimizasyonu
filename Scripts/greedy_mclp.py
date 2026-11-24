from collections import defaultdict

p = QgsProject.instance()

talep = next(
    l for l in p.mapLayers().values()
    if l.name() == "mclp_kapsama_disi_talep_noktalari_nokta2"
)

od = next(
    l for l in p.mapLayers().values()
    if "mclp_talep_aday_durak_yuru" in l.name()
)

# Talep noktalarının nüfus ağırlıkları
nufuslar = {
    int(f["fid"]): int(f["nufus"])
    for f in talep.getFeatures()
}

# Her adayın 400 m içinde kapsadığı talep noktaları
aday_kapsama = defaultdict(set)

for f in od.getFeatures():
    mesafe = float(f["total_cost"])

    if mesafe <= 400:
        aday_id = int(f["destination_id"])
        talep_id = int(f["origin_id"])
        aday_kapsama[aday_id].add(talep_id)

# Greedy MCLP
kapsanan = set()
secimler = []

for sira in range(1, 11):
    en_iyi_aday = None
    en_iyi_nufus = 0
    en_iyi_yeni_talepler = set()

    for aday_id, talepler in aday_kapsama.items():
        if aday_id in secimler:
            continue

        yeni_talepler = talepler - kapsanan
        kazanilan_nufus = sum(
            nufuslar[t] for t in yeni_talepler
        )

        if kazanilan_nufus > en_iyi_nufus:
            en_iyi_aday = aday_id
            en_iyi_nufus = kazanilan_nufus
            en_iyi_yeni_talepler = yeni_talepler

    if en_iyi_aday is None:
        break

    secimler.append(en_iyi_aday)
    kapsanan.update(en_iyi_yeni_talepler)

    print(
        sira,
        "Aday FID:", en_iyi_aday,
        "Yeni kapsanan nüfus:", en_iyi_nufus,
        "Toplam kapsanan nüfus:",
        sum(nufuslar[t] for t in kapsanan)
    )

print("\nSeçilen durak sayısı:", len(secimler))
print("Seçilen aday FID'leri:", secimler)
print("Kapsanan talep noktası:", len(kapsanan), "/ 12")
print(
    "Kapsanan nüfus:",
    sum(nufuslar[t] for t in kapsanan)
)
print(
    "Kapsama oranı:",
    round(
        100 * sum(nufuslar[t] for t in kapsanan)
        / sum(nufuslar.values()), 2
    ),
    "%"
)