from google import genai
from google.genai import types
import streamlit as st
import warnings

warnings.filterwarnings("ignore")

client = genai.Client(api_key="AIzaSyDxM24oJ67m_RpCYaQhiq9lX7XuUfZbIHQ")

st.set_page_config(page_title="STenta-Masterclass AI", page_icon="🎓", layout="wide")

st.title("🎓 Tenta-Masterclass AI")
st.write("Ladda upp föreläsningen och få djupförståelse")

if "result_text" not in st.session_state:
     st.session_state.result_text = None


uploaded_file = st.file_uploader("Välj en PDF-fil", type=["pdf"])

if uploaded_file:
    st.success("✅ Filen '{uploaded_file.name}' är redo!")
    
    if st.button("Skapa Tenta-Masterclass ✨", use_container_width=True):
            with st.spinner("Professor Gemini analyseras föreläsningen..."):
                    
                instruktion = """

                Du är en erfaren universitetsprofessor som förbereder studenter inför en svår tenta. 
                Din uppgift är att analysera den bifogade föreläsningen och skapa en "Tenta-Masterclass".

                Följ denna struktur för varje viktigt område:

                1. Kritiska Koncept: Identifiera de absolut viktigaste delarna som sannolikt kommer på tentan.
                2. Djupdykning: Förklara teorin bakom dessa delar på ett djupt men pedagogiskt sätt. 
                Om det nämns matematiska regler (som t.ex. Squeeze Theorem), förklara LOGIKEN bakom dem, 
                inte bara formeln. Varför fungerar det?
                3. Steg-för-steg Metodik: Hur löser man ett problem inom detta område? Ge en 1-2-3-guide.
                4. "Tenta-fällan": Vilka vanliga fel gör studenter här? Vad ska jag se upp för?
                5. Praktiskt räkneexempel: Visa ett konkret exempel från föreläsningen eller ett liknande tal, 
                och lös det steg för steg med tydliga förklaringar.

                Använd rubriker, fetstil och punktlistor för att göra svaret extremt lättläst i Markdown.

                6. Självtest: Skapa 3-5 utmanande frågor baserat på föreläsningen.
                    - För räkneuppgifter: Ange talet och beskriv vad som ska lösas.
                    - För teori: Ställ en öppen fråga om koncepten eller logiken.
   
                Viktigt: Lägg svaren på frågorna längst ner under en rubrik som heter 'FACIT', så att studenten inte ser dem direkt.

                """

                file_bytes = uploaded_file.getvalue()

                content_payload = [
                     instruktion, 
                     types.Part.from_bytes(data=file_bytes, mime_type = "application/pdf")
                     ]
                
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=content_payload
                    )
                    st.session_state.result_text = response.text
                except Exception as e:
                     st.error(f"Ett fel uppstod vid analysen: {e}")

if st.session_state.result_text:
    st.divider()
    st.success("Analysen är klar!")
  
    full_text = st.session_state.result_text

    if "FACIT" in full_text:
         main_content, facit_content = full_text.split("FACIT", 1)

         main_content = main_content.replace("<br>", "\n").strip()
         facit_content = facit_content.replace("<br>", "\n").strip()
    else:
         main_content = full_text
         facit_content = "Inget facit hittades."
    
    st.markdown(main_content)

    st.download_button(
        label="💾 Ladda ner Masterclass (inkl. facit) som .md",
        data=st.session_state.result_text,
        file_name="tenta_masterclass.md",
        mime="text/markdown"
    )

    st.divider()

    st.subheader("🧠 Testa dina kunskaper")
    user_answer = st.text_area("Skriv ditt svar på en av frågorna ovan så rättar jag det:")

    if st.button("Rätta mitt svar"):
        if user_answer:
            with st.spinner("Professor Gemini rättar..."):
                rattnings_prompt = f"""
                Här är en sammanfattning av en föreläsning: {main_content}
                                        
                En student har svarat följande på en av frågorna: "{user_answer}"
                                        
                Din uppgift:
                1. Avgör om svaret är rätt, delvis rätt eller fel.
                2. Om det är matte: Visa uträkningen steg-för-steg.
                3. Om det är teori: Förklara vad som var bra och vad som saknades.                               
                4. Var uppmuntrande men pedagogiskt sträng!
                """

                correction = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[rattnings_prompt]
                )
                st.info("Rättning:")
                st.write(correction.text)
        else:
             st.warning("Skriv ett svar först!")
    st.divider()

    with st.expander("Se Faceit (Klicka här när du är klar)"):
         st.markdown(facit_content)
            
else:
    if not uploaded_file:
        st.info("Börja med att ladda upp en föreläsning ovan")
