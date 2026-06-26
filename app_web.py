import streamlit as st
import json

# Sayfa Yapılandırması (Mobil ve PC için geniş ekran ayarı)
st.set_page_config(page_title="Sınav Hazırlık Platformu", page_icon="📝", layout="centered")

# Soruları JSON dosyasından otomatik çekiyoruz
if "soru_havuzu" not in st.session_state:
    try:
        with open("sorular.json", "r", encoding="utf-8") as f:
            st.session_state.soru_havuzu = json.load(f)
    except FileNotFoundError:
        st.error("sorular.json dosyası bulunamadı! Lütfen dosyanın bu klasörde olduğundan emin olun.")
        st.session_state.soru_havuzu = {}

# Uygulama Durum Değişkenleri (Session State)
if "mevcut_soru_index" not in st.session_state:
    st.session_state.mevcut_soru_index = 0
if "cevaplandi" not in st.session_state:
    st.session_state.cevaplandi = False
if "secilen_cevap" not in st.session_state:
    st.session_state.secilen_cevap = None

# Başlık ve Tasarım
st.markdown("<h1 style='text-align: center; color: #24a0ed;'>Sınav Hazırlık Platformu</h1>", unsafe_allow_html=True)

if st.session_state.soru_havuzu:
    # Sol Menü Üst Kısım: Branş Seçimi
    mevcut_brans = st.sidebar.selectbox("Lütfen Branş Seçin:", list(st.session_state.soru_havuzu.keys()))

    # Eğer branş değişirse indexi sıfırla
    if "eski_brans" not in st.session_state or st.session_state.eski_brans != mevcut_brans:
        st.session_state.eski_brans = mevcut_brans
        st.session_state.mevcut_soru_index = 0
        st.session_state.cevaplandi = False
        st.session_state.secilen_cevap = None

    sorular = st.session_state.soru_havuzu[mevcut_brans]
    toplam_soru = len(sorular)

    # --- YENİ EKLENEN KISIM: YAN MENÜDE SORU LİSTESİ ---
    st.sidebar.write("---")
    st.sidebar.markdown("### 🔍 Soru Navigasyonu")
    
    # Kullanıcının listeden rahatça seçmesi için "1. Soru", "2. Soru" gibi bir liste hazırlıyoruz
    soru_listesi = [f"{i+1}. Soru" for i in range(toplam_soru)]
    
    # Kullanıcı yan menüden bir soru seçtiğinde tetiklenir
    secilen_soru_str = st.sidebar.radio(
        "Gitmek istediğiniz soruyu seçin:", 
        soru_listesi, 
        index=st.session_state.mevcut_soru_index,
        key="soru_navigasyon_radyo"
    )
    
    # Seçilen string ifadeden index numarasını ayıklıyoruz (Örn: "50. Soru" -> 49)
    yeni_index = soru_listesi.index(secilen_soru_str)
    
    # Eğer kullanıcı yan menüden başka bir soruya tıkladıysa konumu değiştir ve durumu sıfırla
    if yeni_index != st.session_state.mevcut_soru_index:
        st.session_state.mevcut_soru_index = yeni_index
        st.session_state.cevaplandi = False
        st.session_state.secilen_cevap = None
        st.rerun()
    # --------------------------------------------------

    if st.session_state.mevcut_soru_index < toplam_soru:
        soru_data = sorular[st.session_state.mevcut_soru_index]
        
        # Soru Kartı
        st.info(f"**Branş:** {mevcut_brans} | **Soru:** {st.session_state.mevcut_soru_index + 1} / {toplam_soru}")
        st.subheader(soru_data["soru"])
        
        # Şıkların Buton Olarak Basılması
        for secenek in soru_data["secenekler"]:
            if st.button(secenek, key=secenek, use_container_width=True, disabled=st.session_state.cevaplandi):
                st.session_state.secilen_cevap = secenek
                st.session_state.cevaplandi = True
                st.rerun()
                
        # Cevap Kontrol Alanı
        if st.session_state.cevaplandi:
            dogru_cevap = soru_data["cevap"].strip()
            if st.session_state.secilen_cevap == dogru_cevap:
                st.success(f"🎉 Doğru Cevap! Seçtiğiniz: {st.session_state.secilen_cevap}")
            else:
                st.error(f"❌ Yanlış Cevap! Doğru Şık: {dogru_cevap}")
                st.warning(f"Sizin Seçtiğiniz: {st.session_state.secilen_cevap}")
                
            if st.button("Sonraki Soruya Geç ➔", type="primary"):
                st.session_state.mevcut_soru_index += 1
                st.session_state.cevaplandi = False
                st.session_state.secilen_cevap = None
                st.rerun()
                
        # Alt Gezinme Barı
        st.write("---")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.session_state.mevcut_soru_index > 0:
                if st.button("🡨 Önceki Soru"):
                    st.session_state.mevcut_soru_index -= 1
                    st.session_state.cevaplandi = False
                    st.session_state.secilen_cevap = None
                    st.rerun()
    else:
        st.balloons()
        st.success("🎉 Tebrikler! Bu branştaki tüm soruları başarıyla tamamladınız.")
        if st.button("Branşı Yeniden Başlat 🗘"):
            st.session_state.mevcut_soru_index = 0
            st.session_state.cevaplandi = False
            st.session_state.secilen_cevap = None
            st.rerun()