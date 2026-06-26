import streamlit as st
import json
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="Sınav Hazırlık Platformu", page_icon="📝", layout="centered")

# Soruları JSON dosyasından çekme
if "soru_havuzu" not in st.session_state:
    try:
        with open("sorular.json", "r", encoding="utf-8") as f:
            st.session_state.soru_havuzu = json.load(f)
    except FileNotFoundError:
        st.error("sorular.json dosyası bulunamadı!")
        st.session_state.soru_havuzu = {}

# Uygulama Hafıza Değişkenleri
if "mevcut_soru_index" not in st.session_state:
    st.session_state.mevcut_soru_index = 0
if "cevap_durumu" not in st.session_state:
    st.session_state.cevap_durumu = None # None, "dogru", "yanlis"

# Başlık
st.markdown("<h1 style='text-align: center; color: #24a0ed;'>Sınav Hazırlık Platformu</h1>", unsafe_allow_html=True)

if st.session_state.soru_havuzu:
    # Sol Menü: Branş Seçimi
    mevcut_brans = st.sidebar.selectbox("Lütfen Branş Seçin:", list(st.session_state.soru_havuzu.keys()))

    # Branş değişirse durumu sıfırla
    if "eski_brans" not in st.session_state or st.session_state.eski_brans != mevcut_brans:
        st.session_state.eski_brans = mevcut_brans
        st.session_state.mevcut_soru_index = 0
        st.session_state.cevap_durumu = None
        st.rerun()

    sorular = st.session_state.soru_havuzu[mevcut_brans]
    toplam_soru = len(sorular)

    # Sol Menü: İstediğin Soruya Atla
    st.sidebar.write("---")
    st.sidebar.markdown("### 🔍 İstediğin Soruya Atla")
    
    hedef_soru = st.sidebar.number_input(
        f"Soru Numarası (1 - {toplam_soru}):", 
        min_value=1, 
        max_value=toplam_soru, 
        value=st.session_state.mevcut_soru_index + 1,
        step=1
    )
    
    if hedef_soru - 1 != st.session_state.mevcut_soru_index:
        st.session_state.mevcut_soru_index = hedef_soru - 1
        st.session_state.cevap_durumu = None
        st.rerun()

    # Sol Alt Köşeye İmza
    st.sidebar.write("---")
    st.sidebar.markdown(
        "<div style='position: fixed; bottom: 20px; left: 20px; font-weight: bold; color: #24a0ed; font-size: 16px;'>"
        "👨‍💻 Mehmet Gökpınar"
        "</div>", 
        unsafe_allow_html=True
    )

    # Ana Soru Ekranı
    if st.session_state.mevcut_soru_index < toplam_soru:
        soru_data = sorular[st.session_state.mevcut_soru_index]
        
        st.info(f"**Branş:** {mevcut_brans} | **Soru:** {st.session_state.mevcut_soru_index + 1} / {toplam_soru}")
        st.subheader(soru_data["soru"])
        
        # Şık Seçim Alanı (Eğer cevaplandıysa kilitlenir)
        kilitli_mi = st.session_state.cevap_durumu is not None
        secim = st.radio(
            "Cevabınızı seçin:", 
            soru_data["secenekler"], 
            key=f"r_{mevcut_brans}_{st.session_state.mevcut_soru_index}",
            disabled=kilitli_mi
        )
        
        st.write("---")
        
        # Ekranda Kontrol Butonu Gösterimi
        if st.session_state.cevap_durumu is None:
            if st.button("Cevabı Onayla ✔️", type="primary", use_container_width=True):
                dogru_cevap = soru_data["cevap"].strip()
                
                if secim.strip() == dogru_cevap:
                    st.session_state.cevap_durumu = "dogru"
                    st.rerun()
                else:
                    st.session_state.cevap_durumu = "yanlis"
                    st.rerun()
                    
        # GERİ BİLDİRİM VE İLERLEME MANTIĞI
        if st.session_state.cevap_durumu == "dogru":
            st.success("🎉 Doğru Cevap! 1 saniye sonra sonraki soruya geçiliyor...")
            time.sleep(1)
            st.session_state.mevcut_soru_index += 1
            st.session_state.cevap_durumu = None
            st.rerun()
            
        elif st.session_state.cevap_durumu == "yanlis":
            st.error(f"❌ Yanlış Cevap! Doğru Şık: {soru_data['cevap'].strip()}")
            
            # Yanlış yapınca buradaki butona basana kadar sayfada kalır
            if st.button("Sonraki Soru ➔", type="primary", use_container_width=True):
                st.session_state.mevcut_soru_index += 1
                st.session_state.cevap_durumu = None
                st.rerun()
                
        # Önceki Soruya Dönme Butonu
        if st.session_state.mevcut_soru_index > 0 and st.session_state.cevap_durumu is None:
            if st.button("🡨 Önceki Soruya Dön", use_container_width=True):
                st.session_state.mevcut_soru_index -= 1
                st.session_state.cevap_durumu = None
                st.rerun()
    else:
        st.balloons()
        st.success("🎉 Tebrikler! Bu branştaki tüm soruları başarıyla tamamladınız.")
        if st.button("Branşı Yeniden Başlat 🗘", use_container_width=True):
            st.session_state.mevcut_soru_index = 0
            st.session_state.cevap_durumu = None
            st.rerun()