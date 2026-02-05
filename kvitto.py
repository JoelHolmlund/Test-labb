import streamlit as st
from google import genai
from google.genai import types
import warnings
from PIL import Image
import io

warnings.filterwarnings("ignore")

# Setup Gemini
client = genai.Client(api_key="AIzaSyCWNOvl1WTnp_MicqJ13tvWlNnkLI1YxcM")

st.set_page_config(page_title="AI Ekonomi-Assistent", layout="wide")

# --- DATABASE / STATE LOGIC ---
# Vi skapar en plats att spara all historik om den inte redan finns
if "db" not in st.session_state:
    st.session_state.db = {} # Format: {"Namn": [lista med kvitton]}

# --- LOGIN ---
if "user" not in st.session_state:
    st.title("Välkommen till AI-Ekonomen 🧾")
    username = st.text_input("Skriv in ditt namn för att börja:")
    if st.button("Logga in"):
        if username:
            st.session_state.user = username
            if username not in st.session_state.db:
                st.session_state.db[username] = []
            st.rerun()
    st.stop()

# --- APP INTERFACE (Efter inloggning) ---
user = st.session_state.user

# SIDEBAR: Historik
with st.sidebar:
    st.title(f"Inloggad som: {user}")
    if st.button("Logga ut"):
        del st.session_state.user
        st.rerun()
    
    st.divider()
    st.header("Din historik")
    user_history = st.session_state.db.get(user, [])
    
    if not user_history:
        st.write("Inga sparade kvitton än.")
    else:
        for entry in reversed(user_history): # Visa senaste först
            with st.expander(f"{entry['datum']} - {entry['butik']}"):
                st.write(f"**Pris:** {entry['pris']}")
                st.caption(f"Artikelnummer: {entry['Artikelnummer']}")

# MAIN AREA: Skanner
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Ladda upp kvitto")
    uploaded_file = st.file_uploader("Bild eller PDF", type=["jpg", "jpeg", "png", "pdf"])
    
    if uploaded_file:
        is_pdf = uploaded_file.type == "application/pdf"
        if is_pdf:
            file_to_send = uploaded_file.getvalue()
            st.info("PDF redo för analys.")
        else:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            file_to_send = image

        if st.button("Analysera och Spara ✨"):
            with st.spinner("AI-Ekonomen läser av..."):
                instruktion = """
                Analysera detta kvitto. Svara ENDAST med ett kortfattat resultat i detta format:
                Butik: [Namn]
                Datum: [ÅÅÅÅ-MM-DD]
                Pris: [Summa + Valuta]
                Artikelnummer: [EAN]
                """
                
                if is_pdf:
                    content_payload = [instruktion, types.Part.from_bytes(data=file_to_send, mime_type="application/pdf")]
                else:
                    content_payload = [instruktion, file_to_send]

                response = client.models.generate_content(model="gemini-3-flash-preview", contents=content_payload)
                
                # Spara till vår "databas"
                result_text = response.text
                
                # Enkel logik för att dra ut info till sidomenyn (skulle kunna göras proffsigare med JSON)
                lines = result_text.split('\n')
                entry = {
                    "butik": lines[0].replace("Butik: ", ""),
                    "datum": lines[1].replace("Datum: ", ""),
                    "pris": lines[2].replace("Pris: ", ""),
                    "Artikelnummer": lines[3].replace("Artikelnummer: ", "")
                }
                st.session_state.db[user].append(entry)
                
                st.session_state.last_result = result_text
                st.rerun()

with col2:
    st.header("Senaste resultat")
    if "last_result" in st.session_state:
        st.success("Kvitto avläst!")
        st.markdown(st.session_state.last_result)
    else:
        st.write("Ladda upp ett kvitto för att se analysen här.")