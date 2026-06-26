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

# Uygulama Durum Değişkenleri (Hafıza Yönetimi)
if "mevcut_soru_index" not in st.session_state:
    st.session_state.mevcut_soru_index = 0

# Başlık
st.markdown("<h1 style='text-align: center; color: #24a0ed;'>Sınav Hazırlık Platformu</h1>", unsafe_allow_html=True)

if st.session_state.soru_havuzu:
    # Sol Menü Üst Kısım: Branş Seçimi
    mevcut_brans = st.sidebar.selectbox("Lütfen Branş Seçin:", list(st.session_state.soru_havuzu.keys()))

    # Eğer branş değişirse durumu sıfırla
    if "eski_brans" not in st.session_state or st.session_state.eski_brans != mevcut_brans:
        st.session_state.eski_brans = mevcut_brans
        st.session_state.mevcut_soru_index = 0
        st.rerun()

    sorular = st.session_state.soru_havuzu[mevcut_brans]
    toplam_soru = len(sorular)

    # Yan Menü Soru Navigasyonu
    st.sidebar.write("---")
    st.sidebar.markdown("### 🔍 Soru Navigasyonu")
    soru_listesi = [f"{i+1}. Soru" for i in range(toplam_soru)]
    
    secilen_soru_str = st.sidebar.radio(
        "Gitmek istediğiniz soruyu seçin:", 
        soru_listesi, 
        index=st.session_state.mevcut_soru_index,
        key="nav_radio"
    )
    
    yeni_index = soru_listesi.index(secilen_soru_str)
    if yeni_index != st.session_state.mevcut_soru_index:
        st.session_state.mevcut_soru_index = yeni_index
        st.rerun()

    # Ana Soru Alanı
    if st.session_state.mevcut_soru_index < toplam_soru:
        soru_data = shortages = sorular[st.session_state.mevcut_soru_index]
        
        st.info(f"**Branş:** {mevcut_brans} | **Soru:** {st.session_state.mevcut_soru_index + 1} / {toplam_soru}")
        st.subheader(soru_data["soru"])
        
        # Web için En Güvenli Şık Seçim Alanı (Takılmayı engeller)
        secim = st.radio("Cevabınızı seçin:", soru_data["secenekler"], key=f"soru_{st.session_state.mevcut_soru_index}")
        
        # Kontrol Et ve İlerleme Butonları yan yana
        col_kontrol, col_sonraki = st.columns(2)
        
        with col_kontrol:
            if st.button("Cevabı Kontrol Et ✔️", use_container_width=True):
                dogru_cevap = soru_data["cevap"].strip()
                if secim.strip() == dogru_cevap:
                    st.success(f"🎉 Doğru Cevap!")
                else:
                    st.error(f"❌ Yanlış Cevap! Doğru Şık: {dogru_cevap}")

        with col_sonraki:
            if st.button("Sonraki Soruya Geç ➔", type="primary", use_container_width=True):
                st.session_state.mevcut_soru_index += 1
                st.rerun()
                
        # Alt Gezinme Barı (Önceki Soru)
        st.write("---")
        if st.session_state.mevcut_soru_index > 0:
            if st.button("🡨 Önceki Soru"):
                st.session_state.mevcut_soru_index -= 1
                st.rerun()
    else:
        st.balloons()
        st.success("🎉 Tebrikler! Bu branştaki tüm soruları başarıyla tamamladınız.")
        if st.button("Branşı Yeniden Başlat 🗘"):
            st.session_state.mevcut_soru_index = 0
            st.rerun()