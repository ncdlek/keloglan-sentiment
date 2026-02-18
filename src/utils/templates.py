# --- EVRENSEL KATEGORILER (Trendyol, E-Ticaret, Okul) ---
fashion_items = ["Kumaşı", "Dikişleri", "Rengi", "Kalıbı", "Elbise", "Pantolon", "Ayakkabı"]
fashion_neg = ["naylon gibi", "iç gösteriyor", "pot durdu", "sökük geldi", "resmen çöp", "bedeni uymadı", "renk soluk"]
fashion_pos = ["efsane", "tam oturdu", "manken gibi durdu", "pamuk gibi", "yumuşacık", "bayıldım"]

cosmetic_items = ["Ruj", "Fondöten", "Krem", "Maskara", "Parfüm", "Serum"]
cosmetic_neg = ["sivilce yaptı", "alerji yaptı", "kalıcılığı yok", "pul pul döküldü", "kokusu ağır", "yapış yapış"]
cosmetic_pos = ["bebek gibi yaptı", "ışıl ışıl", "kokusu harika", "gün boyu kaldı", "vazgeçilmezim"]

tech_items = ["Telefon", "Bilgisayar", "Kulaklık", "Batarya", "Ekran", "FPS"]
tech_neg = ["ısınıyor", "donuyor", "şarjı su gibi içiyor", "piksel piksel", "ses boğuk", "kasıyor"]
tech_pos = ["uçuyor", "canavar gibi", "şarjı bitmiyor", "ses kalitesi müthiş", "f/p ürünü"]

student_context = ["Vize", "Final", "Büt", "Hoca", "KYK yurdu", "Yemekhane", "Burs"]
student_neg = ["yine bitti", "taktı bana", "zehirledi", "yatmadı", "sıcak su yok", "internet çekmiyor", "sabahladım"]
student_pos = ["geçtim", "aa düştü", "efsane çıktı", "yattı sonunda", "yemekler güzeldi"]

art_items = ["Senaryo", "Oyunculuk", "Final", "Kurgu", "Ses sistemi", "Konser", "Albüm"]
art_neg = ["çöp", "yapay", "hayal kırıklığı", "klişe", "patlıyor", "playback yaptı", "vakit kaybı"]
art_pos = ["ters köşe", "oscar'lık", "ağlattı", "tüyler diken", "sahne şovu efsane", "döktürmüş"]

secondhand_neg = [
    "Ölücüler yazmasın kalbini kırarım.",
    "Sıfır diye sattı, haşat çıktı.",
    "Kargoyu alıcı öder dediler, kandırdılar.",
    "Dolandırıcı dikkat edin.",
    "Ürün pert, açıklamada yazmıyordu."
]
secondhand_pos = [
    "Sıfır ayarında, tertemiz.",
    "Jelatini üstünde.",
    "Güvenilir satıcı, hediye de yollamış.",
    "Sorunsuz alışveriş, teşekkürler."
]

neutral_statements = [
    "Kargo bugün saat 14:00'te teslim edildi.",
    "Paket şubeye ulaşmış, yarın alacağım.",
    "Ürünün kutusundan garanti belgesi çıkıyor.",
    "Rengi görseldeki gibi mavi.",
    "Henüz deneme fırsatım olmadı, sonra yazacağım.",
    "Siparişi verdim, bekliyorum.",
    "Film yaklaşık 2 saat sürüyor.",
    "Mağaza sabah 09:00'da açılıyor.",
    "Ürün 2 yıl garantiliymiş.",
    "Kurulumu servis yapıyor.",
    "Fiyatı piyasa ortalamasında.",
    "Kullanma kılavuzu Türkçe.",
    "Bakalım göreceğiz, inşallah iyidir.",
    "Daha kutuyu açmadım.",
    "Şarj kablosu Type-C uyumlu."
]

ks_neg = [
    "Ghostladı beni, cevap vermiyor.",
    "Tam bir red flag, koşarak kaç.",
    "Toxic ilişki bu, seni bitirir.",
    "Aldattı sandım, meğer yalanmış.",
    "Linçlemeyin ama bence haksızsın.",
    "Trip atıyor sürekli, bıktım."
]
ks_pos = [
    "Shipledim sizi, çok yakıştınız.",
    "Bence sana aşık, belli ediyor.",
    "Green flag resmen, kaçırma.",
    "KS halkı olarak arkandayız.",
    "Enişte doğru söylüyor."
]

# --- KÜLTÜREL VE DERİN BAĞLAM ---
cultural_irony = [
    "Silivri şimdi soğuktur, hiç konuşmayalım en iyisi.",
    "Ekonomi uçuyor şahlanıyoruz maşallah (!) ",
    "Maaş yattığı saniye eridi, tebrikler büyük başarı.",
    "Ampul patladı artık karanlıktayız.",
    "Adalet mülkün temeliydi ama temel çatlamış.",
    "Porsiyonlar küçülmüş ama fiyatlar büyümüş, şahane.",
    "Kendi uçağımızı yapıyorduk hani? Hala otobüs bekliyoruz.",
    "Liyakat yerlerde, torpil göklerde.",
    "Gözlerimdeki ışıltıyı görüyor musun? Ben göremiyorum.",
    "Silivri yolu göründü bize bu gidişle.",
    "Millet aç aç, neyin kafası bu?",
    "Zam değil güncelleme canım o (!)",
    "Avrupa bizi kıskanıyor, kesin öyledir.",
    "Etiketi görünce tansiyonum düştü resmen.",
    "Markete girince moralim bozuluyor, her şey ateş pahası.",
    "Dolarla mı maaş alıyorsun sanki (!)",
    "Kemer sıkmaktan belimiz koptu."
]

daily_struggles = [
    "Metrobüs yine balık istifi, nefes alamadık.",
    "Köprü trafiği kilit, 2 saattir adım atılmıyor.",
    "Taksi bulmak imkansız, hepsi turist peşinde.",
    "İnternetim o kadar yavaş ki dumanla haberleşsem daha hızlı.",
    "AKK doldu galiba, sayfa açılmıyor.",
    "Pingim 999 oldu, oyun oynanmıyor.",
    "Hoca taktı bana, yine dersten bıraktı.",
    "Bütlere kaldık, tatil yalan oldu.",
    "KYK yatmadı mı hala, aç kaldık.",
    "Yemekhane yemeğinden taş çıktı, dişimi kırdım.",
    "Kargom şubede kaybolmuş, muhatap yok."
]

sports_neg = [
    "Hakem maçı katletti, göz göre göre doğradı bizi.",
    "Yönetim istifa! Yeter artık sabrımız kalmadı.",
    "Bu takımdan bir cacık olmaz, kanser ettiniz bizi.",
    "Yine hüsran, yine mağlubiyet. Alıştık artık.",
    "O paraları hak etmiyorsunuz, yazıklar olsun."
]

context_neg = [
    "Resmen taş devri teknolojisi kullanıyorsunuz.",
    "Kağnı hızıyla çalışan bir sistem yapmışsınız, bravo.",
    "Bu hizmet tam bir fiyasko, dağ fare doğurdu.",
    "Görüntü var ses yok, içi boş bir ürün.",
    "Paramızla rezil olduk, başka bir şey değil.",
    "Verdiğim para haram zıkkım olsun.",
    "Bin pişman oldum aldığıma, elimde patladı.",
    "Resmen insanla dalga geçiyorlar.",
    "Boşa kürek çekmişiz, hiçbir işe yaramıyor.",
    "Sıfır ilgi, sıfır alaka, sıfır hizmet.",
    "Tam bir hayal kırıklığı, param çöp oldu.",
    "Dimyata pirince giderken evdeki bulgurdan olduk.",
    "Astarı yüzünden pahalıya geldi.",
    "İş işten geçti artık, geçmiş olsun."
]

cultural_pos = [
    "Musluktan rakı akıyor mübarek, bu ne keyif!",
    "Adamlar yapmış abi, helal olsun.",
    "Gözüm kapalı tavsiye ederim, efsane bir şey.",
    "Yediğim en iyi yemekti, ellerine sağlık usta.",
    "Hızır gibi yetiştiler, çok teşekkürler.",
    "Allah razı olsun, mağduriyetimi hemen giderdiler.",
    "Krallar gibi karşılandık, hizmet on numara.",
    "Kalitenin tek adresi, şaşmam artık.",
    "Cillop gibi ürün, pırıl pırıl geldi.",
    "Sonuna kadar hak ediyorlar, helal-i hoş olsun.",
    "On numara beş yıldız, eksiksiz hizmet.",
    "Lokum gibi et, ağızda dağılıyor.",
    "Taş gibi sağlam, ömürlük kullanırsın.",
    "Bu sene o sene, şampiyonluk geliyor!"
]

rel_slang = [
    "Ghostladı beni resmen, cevap bile vermiyor.", # Neg
    "Tam bir toxic ilişki, uzak dur.", # Neg
    "Red flag veriyor, koşarak kaç.", # Neg
    "Shipledim sizi, çok yakıştınız.", # Pos
    "Stalk yapmaktan ciğerim soldu.", # Notr/Neg
    "Vibe'ı çok kötü, enerjimi emdi.", # Neg
    "Date'e çıktık tam bir fiyaskoydu.", # Neg
    "Manita yaptı bizi unuttu.", # Neg
    "Aşırı cringe bir ortam, dayanamadım.", # Neg
    "Moodum düştü yine."
]

gamer_slang = [
    "Takım kolsuz dolu, kanser oldum.", # Neg (0)
    "Tek yedi resmen, ezdim geçtim.", # Pos (2)
    "Maçı tek başıma carryledim.", # Pos (2)
    "Lagdan oyun oynanmıyor, sunucular patates.", # Neg (0)
    "NPC gibi yaşıyorum, hayat çok sıkıcı.", # Neg (0)
    "Bug dolu oyun, verdiğim paraya yazık.", # Neg (0)
    "Grafikler efsane, bayıldım.", # Pos (2)
    "Hile dolu, raporladım banlanmadı.", # Neg (0)
    "GG WP, güzel maçtı."
]

food_hate = [
    "Mide fesadı geçirdim, zehirlediniz beni.",
    "Bulaşık suyu gibi kahve, içilmiyor.",
    "Taş gibi ekmek, dişimi kıracaktım.",
    "Yağ içinde yüzüyor yemek, rezalet.",
    "Çiğ gelmiş tavuk, gıdaklıyordu tabakta.",
    "Buz gibi geldi, dondurma sandım.",
    "Sanki nimet değil zulüm yiyoruz."
]

life_struggle = [
    "Hayat bitti biz okey dönüyoruz.",
    "Coğrafya kaderdir dediler, kandırdılar.",
    "Yine yangınlar yine ben.",
    "Dert babası olduk iyice.",
    "Ümidimi kestim artık her şeyden.",
    "Sabır taşı olsa çatlardı be."
]

# --- HARD IRONI ---
irony_templates = [
    "Siparişim {time} saatte geldi, bu hız için (!) tebrikler.",
    "Yemek o kadar {adjective} ki dişimi kırdım, harika!",
    "Müşteri hizmetleri yüzüme kapattı, ilgi alaka müthiş!",
    "Ürün paramparça geldi, paketleme sanat eseri resmen.",
    "İnternetim o kadar hızlı ki (!) Google'ı 5 dakikada açıyor.",
    "Buz gibi pizza için teşekkürler, tam istediğim gibi (!) yanmış.",
    "Kargom kayboldu, bu ne güzel bir sürpriz.",
    "Telefonu servise verdim, bozuk geri aldım. Şahane hizmet.",
    "Odamda hamam böcekleriyle partiliyoruz, otel harika (!)",
    "Fiyatlar çok uygun (!) bir böbrek bırakmanız yeterli.",
    "Tebrikler, bu kadar kötü yapmayı nasıl başardınız?",
    "Uygulama sürekli çöküyor, bayıldım bu özelliğe.",
    "Soğuk kahve istemiştim, sıcak geldi. Tam ters köşe, bravo.",
    "Hiçbir sorunumu çözmediniz, varlığınız için teşekkürler (!)"
]

times = ["3", "5", "10", "24", "48"]
adjectives = ["sert", "bayat", "kötü", "taş gibi"]

# --- NOISE / GÜRÜLTÜ ---
noise_texts = [
    "...", "..", "?", "??", "ok", "tm", "tmm", "slm", "mrb", 
    "q", "w", "asdf", "test", "deneme", "123", 
    "       ", " ", "\n", ".", ",", "a", "b", "c",
    "aynen", "tabii", "geldi", "bakalim"
]

pos_emojis = ["😍", "🔥", "❤️", "🥰", "🤩", "👍", "👏", "💯", "🚀"]
neg_emojis = ["😡", "🤬", "👎", "🤮", "🤢", "😤", "💩", "💔", "🙄"]
