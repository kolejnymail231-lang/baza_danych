import streamlit as st
from supabase import create_client, Client

# 1. Konfiguracja połączenia z Supabase
# W produkcji użyj st.secrets["SUPABASE_URL"]
SUPABASE_URL = "https://rvmohidljplctnckdwvo.supabase.co"
SUPABASE_KEY = "sb_publishable_Ctl7It5WKwmVMBtbyshyIA_2WDFALsV"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Zarządzanie Sklepem", layout="centered")
st.title("📦 System Zarządzania Produktami")

# --- MENU BOCZNE ---
menu = ["Dodaj Produkt", "Dodaj Kategorię", "Podgląd Bazy"]
choice = st.sidebar.selectbox("Nawigacja", menu)

# --- FUNKCJE POMOCNICZE ---
def get_categories():
    response = supabase.table("kategorie").select("id, nazwa").execute()
    return response.data

# --- LOGIKA APLIKACJI ---

if choice == "Dodaj Kategorię":
    st.header("➕ Nowa Kategoria")
    with st.form("form_kategoria"):
        nazwa = st.text_input("Nazwa kategorii")
        opis = st.text_area("Opis")
        submit = st.form_submit_button("Zapisz kategorię")

        if submit:
            if nazwa:
                data = {"nazwa": nazwa, "opis": opis}
                try:
                    supabase.table("kategorie").insert(data).execute()
                    st.success(f"Dodano kategorię: {nazwa}")
                except Exception as e:
                    st.error(f"Błąd: {e}")
            else:
                st.warning("Nazwa jest wymagana!")

elif choice == "Dodaj Produkt":
    st.header("🛍️ Nowy Produkt")
    
    # Pobieramy aktualne kategorie do selectboxa
    kategorie = get_categories()
    if not kategorie:
        st.error("Najpierw dodaj przynajmniej jedną kategorię!")
    else:
        kat_options = {k['nazwa']: k['id'] for k in kategorie}
        
        with st.form("form_produkt"):
            nazwa_prod = st.text_input("Nazwa produktu")
            liczba = st.number_input("Ilość (Liczba)", min_value=0, step=1)
            cena = st.number_input("Cena", min_value=0.0, format="%.2f")
            wybrana_kat_nazwa = st.selectbox("Kategoria", list(kat_options.keys()))
            
            submit_prod = st.form_submit_button("Dodaj produkt")
            
            if submit_prod:
                if nazwa_prod:
                    payload = {
                        "Nazwa": nazwa_prod,
                        "Liczba": liczba,
                        "Cena": cena,
                        "kategorie_id": kat_options[wybrana_kat_nazwa]
                    }
                    try:
                        supabase.table("Produkty").insert(payload).execute()
                        st.success(f"Dodano produkt: {nazwa_prod}")
                    except Exception as e:
                        st.error(f"Błąd zapisu: {e}")
                else:
                    st.warning("Nazwa produktu jest wymagana!")

elif choice == "Podgląd Bazy":
    st.header("📊 Aktualny stan bazy")
    
    col1, col2 = st.tabs(["Produkty", "Kategorie"])
    
    with col1:
        prod_data = supabase.table("Produkty").select("*, kategorie(nazwa)").execute()
        if prod_data.data:
            st.table(prod_data.data)
            
    with col2:
        kat_data = supabase.table("kategorie").select("*").execute()
        if kat_data.data:
            st.table(kat_data.data)
