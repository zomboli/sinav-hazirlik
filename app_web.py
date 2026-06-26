import streamlit as st
import json

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

# Soru İndexini Hafızada Tutma
if "mevcut_soru_index" not in st.session_state:
    st.session_state.mevcut_soru_index = 0

# Başlık
st.markdown("<h1 style='text-align: center; color: #24a0ed;'>Sınav Hazırlık Platformu</h1>", unsafe_allow_html=True)

if st.session_state.soru_havuzu:
    # Sol Menü: Branş Seçimi
    mevcut_brans = st.sidebar.selectbox("Lütfen Branş Seçin:", list(st.session_state.soru_havuzu.keys()))

    # Branş değişirse indexi sıfırla
    if "eski_brans" not in st.session_state or st.session_state.eski_brans != mevcut_brans:
        st.session_state.eski_brans = mevcut_brans
        st.session_state.mevcut_soru_index = 0
        st.rerun()

    sorular = st.session_state.soru_havuzu[mevcut_brans]
    toplam_soru = len(sorular)

    # Sol Menü: Doğrudan Soruya Atlama Alanı (Gelişmiş Sayı Girişi)
    st.sidebar.write("---")
    st.sidebar.markdown("### 🔍 İstediğin Soruya Atla")
    
    # Kullanıcı buraya sayı girerek (Örn: 50 yazarak) direkt o soruya zıplayabilir
    hedef_soru = st.sidebar.number_input(
        f"Soru Numarası (1 - {toplam_soru}):", 
        min_value=1, 
        max_value=toplam_soru, 
        value=st.session_state.mevcut_soru_index + 1,
        step=1
    )
    
    # Eğer girilen sayı mevcut sorudan farklıysa indexi güncelle
    if hedef_soru - 1 != st.session_state.mevcut_soru_index:
        st.session_state.mevcut_soru_index = hedef_soru - 1
        st.rerun()

    # Ana Soru Ekranı
    if st.session_state.mevcut_soru_index < toplam_soru:
        soru_data = shortages = sorular[st.session_state.mevcut_soru_index]
        
        st.info(f"**Branş:** {mevcut_brans} | **Soru:** {st.session_state.mevcut_soru_index + 1} / {toplam_soru}")
        st.subheader(soru_data["soru"])
        
        # KESİN ÇÖZÜM: Form Yapısı Kullanıyoruz. Form içindeki elemanlar asla kilitlenmeye yol açmaz.
        with st.form(key=f"form_soru_{mevcut_brans}_{st.session_state.mevcut_soru_index}"):
            
            # Şık Seçimi
            secim = st.radio("Cevabınızı seçin:", soru_data["secenekler"])
            
            # Formu Onaylama ve İlerleme Butonu
            submit_button = st.form_submit_button(label="Cevabı Onayla ve Sonraki Soruya Geç ➔", type="primary", use_container_width=True)
            
            if submit_button:
                dogru_cevap = soru_data["cevap"].strip()
                # Önce ekrana sonucu basıyoruz
                if secim.strip() == dogru_cevap:
                    st.success("🎉 Doğru Cevap!")
                else:
                    st.error(f"❌ Yanlış Cevap! Doğru Şık: {dogru_cevap}")
                
                # Hafızada bir sonraki soruya geçiş komutu veriyoruz
                st.session_state.mevcut_soru_index += 1
                st.rerun()
                
        # Önceki Soru Butonu (Formun Dışında)
        st.write("---")
        if st.session_state.mevcut_soru_index > 0:
            if st.button("🡨 Önceki Soruya Dön", use_container_width=True):
                st.session_state.mevcut_soru_index -= 1
                st.rerun()
    else:
        st.balloons()
        st.success("🎉 Tebrikler! Bu branştaki tüm soruları başarıyla tamamladınız.")
        if st.button("Branşı Yeniden Başlat 🗘", use_container_width=True):
            st.session_state.mevcut_soru_index = 0
            st.rerun()