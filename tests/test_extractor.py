from app.extractor import extract_text


url = "https://example.com/"

text = extract_text(url)

print(text[:3000])