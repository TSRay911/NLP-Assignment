import google.generativeai as genai


genai.configure(api_key="AIzaSyAK0fUMW6n5Fw0Lq4xT_spYsELwnt503pc")
model = genai.GenerativeModel("gemini-1.5-flash")

myfile = genai.upload_file("sample_audio.mp3")
print(f"{myfile=}")

result = model.generate_content([myfile, "Describe this audio clip"])
print(f"{result.text=}")
