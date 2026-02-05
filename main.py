import warnings
warnings.filterwarnings("ignore")
from google import genai
client = genai.Client(api_key="AIzaSyCWNOvl1WTnp_MicqJ13tvWlNnkLI1YxcM")

def lista_modeller():
    print ("--- Mina tillgängliga modeller ---")
    for model in client.models.list():
        print(f"Namn: {model.name}")
        print (f"Stöder: {model.supported_actions}\n")

def fraga_gemini(fraga):
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=fraga)
    return response.text

lista_modeller()