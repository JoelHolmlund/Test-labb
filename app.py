import streamlit as st
from google import genai
import warnings

warnings.filterwarnings("ignore")

# Setup
client = genai.Client(api_key="AIzaSyCWNOvl1WTnp_MicqJ13tvWlNnkLI1YxcM")

# Webb-design
st.set_page_config(page_title="LinkedIn Generator", page_icon="🚀")
st.title("🚀 LinkedIn-ifieraren")
st.subheader("Gör din vardag till ett proffsigt inlägg")

# Input
anvandar_text = st.text_area("Vad har du gjort idag?", placeholder="T.ex. Åt burgare i skolan...")

if st.button("Skapa episka inlägg! ✨"):
    if anvandar_text:
        with st.spinner("Gemini 3 tänker ut briljanta vinklar..."):
            prompt = f"Du är en LinkedIn-expert. Skapa tre olika inlägg baserat på denna händelse: {anvandar_text}"
            
            # Anropa din fungerande modell
            response = client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=prompt
            )
            
            st.success("Här är dina förslag!")
            st.markdown(response.text)
    else:
        st.error("Du måste skriva något först!")