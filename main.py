import re
import json
from datetime import datetime

# Simulate Obsidian-style decision notes (unstructured/semi-structured)
obsidian_notes = [
    """
# Karar: Yeni Proje Yönetim Aracı Seçimi
Tarih: 2023-10-26
Tags: #proje-yönetimi #araç-seçimi #karar
Context: Mevcut proje yönetim aracımız yetersiz kalıyor, yeni bir çözüm arayışındayız.
Alternatifler: Jira, Trello, Asana, Monday.com
Outcome: Asana'nın esnekliği ve entegrasyon yetenekleri nedeniyle seçilmesine karar verildi.
Riskler: Geçiş süreci zorlu olabilir, ekip adaptasyonu.
""",
    """
# Karar: Uzaktan Çalışma Politikası Güncellemesi
Tarih: 2024-01-15
Tags: #İK #uzaktan-çalışma #politika
Context: Hibrit çalışma modeline geçiş talepleri artıyor.
Alternatifler: Tamamen uzaktan, tamamen ofis, hibrit model.
Outcome: Haftada 2 gün ofis, 3 gün uzaktan çalışma şeklinde hibrit model benimsendi.
Notlar: Çalışan memnuniyeti anketleri yapılacak.
""",
    """
# Karar: Yeni Pazarlama Kampanyası Başlatma
Tarih: 2023-12-01
Tags: #pazarlama #kampanya #ürün-lansmanı
Context: Yeni ürünümüz için geniş çaplı bir pazarlama kampanyasına ihtiyaç var.
Hedef: Pazar payını %5 artırmak.
Outcome: Sosyal medya odaklı, influencer işbirlikli bir kampanya başlatıldı. İlk sonuçlar olumlu.
""",
    """
# Karar: Veritabanı Mimarisi Değişikliği
Tags: #teknoloji #veritabanı #mimari
Context: Mevcut veritabanı performansı ölçeklenebilirlik sorunları yaratıyor.
Outcome: PostgreSQL'den MongoDB'ye geçiş planı onaylandı.
""",
    """
# Karar: Ofis Taşıma
Tarih: 2024-03-10
Context: Mevcut ofis kira sözleşmesi bitiyor, daha uygun maliyetli bir yer aranıyor.
Outcome: Şehir merkezine daha yakın, daha küçük bir ofise taşınma kararı alındı.
Tags: #ofis #yönetim #maliyet
"""
]

# Desired Notion-like structured data schema (conceptual)
# This represents the columns in a Notion database.
# In a real scenario, this would be defined by the Notion database properties.
NOTION_SCHEMA = {
    "Title": str,
    "Date": datetime,
    "Tags": list,
    "OutcomeSummary": str,
    "ContextSummary": str,
    "RawNote": str # To keep the original for reference
}

def extract_structured_data(note_content: str) -> dict:
    """
    Attempts to extract structured data from an Obsidian-style Markdown note.
    This demonstrates the challenge of parsing free-form text into a rigid schema,
    highlighting the friction between flexible note-taking and structured data management.
    """
    data = {
        "Title": None,
        "Date": None,
        "Tags": [],
        "OutcomeSummary": None,
        "ContextSummary": None,
        "RawNote": note_content.strip()
    }

    # --- Illustrating the manual effort and potential fragility of extraction ---

    # Extract Title using regex. This is prone to breaking if note format changes.
    title_match = re.search(r"^#\s*(Karar:\s*.+)$", note_content, re.MULTILINE)
    if title_match:
        data["Title"] = title_match.group(1).replace("Karar:", "").strip()
    else:
        # Fallback for notes with different title formats or missing titles
        first_line = note_content.split('\n')[1].strip() if len(note_content.split('\n')) > 1 else ""
        if first_line and not first_line.startswith('Tags:'):
            data["Title"] = first_line
        else:
            data["Title"] = "Untitled Decision"

    # Extract Date
    date_match = re.search(r"Tarih:\s*(\d{4}-\d{2}-\d{2})", note_content)
    if date_match:
        try:
            data["Date"] = datetime.strptime(date_match.group(1), "%Y-%m-%d").isoformat()
        except ValueError:
            pass # Keep None if date format is invalid

    # Extract Tags
    tags_match = re.search(r"Tags:\s*(#[\w-]+(?:\s*#[\w-]+)*)", note_content)
    if tags_match:
        data["Tags"] = [tag.strip() for tag in tags_match.group(1).split('#') if tag.strip()]

    # Extract Outcome Summary
    outcome_match = re.search(r"Outcome:\s*(.+)", note_content)
    if outcome_match:
        data["OutcomeSummary"] = outcome_match.group(1).strip()

    # Extract Context Summary
    context_match = re.search(r"Context:\s*(.+)", note_content)
    if context_match:
        data["ContextSummary"] = context_match.group(1).strip()

    return data

print("--- Simulating Obsidian Notes to Notion Database Integration ---")
print("This example demonstrates the challenge of extracting structured data from flexible, text-based notes (like Obsidian) into a rigid database schema (like Notion).\n")

notion_database_entries = []

for i, note in enumerate(obsidian_notes):
    print(f"Processing Note {i+1}...")
    # This is where the manual effort and potential for errors lies
    # in bridging unstructured text to structured data.
    structured_entry = extract_structured_data(note)
    notion_database_entries.append(structured_entry)
    print(f"  Extracted Data (simulating Notion row):\n{json.dumps(structured_entry, indent=2, ensure_ascii=False)}\n")

print("\n--- All Processed Entries (Simulated Notion Database) ---")
print(json.dumps(notion_database_entries, indent=2, ensure_ascii=False))

print("\n--- Demonstrating the difficulty of querying unstructured data ---")
print("Imagine trying to find all decisions related to 'project-management' with a 'positive' outcome directly from raw text.")
print("With structured data, it's easier, but requires the initial extraction effort and consistency.")

# Example query on the *extracted* structured data
query_tag = "proje-yönetimi"
query_outcome_keyword = "olumlu" # 'olumlu' means positive in Turkish

print(f"\nQuery: Decisions tagged '{query_tag}' AND outcome contains '{query_outcome_keyword}'")
found_decisions = []
for entry in notion_database_entries:
    # Querying is straightforward once data is structured
    if query_tag in entry["Tags"] and entry["OutcomeSummary"] and query_outcome_keyword in entry["OutcomeSummary"].lower():
        found_decisions.append(entry["Title"])

if found_decisions:
    print(f"  Found: {', '.join(found_decisions)}")
else:
    print("  No matching decisions found.")

print("\nNotice how the extraction logic needs to be robust and specific to each note's format,")
print("highlighting the friction between flexible note-taking and structured data management.")
