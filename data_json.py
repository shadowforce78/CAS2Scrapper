import json

def read_notes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        notes = data.get('relevé', {}).get('ressources', {})
        for module, details in notes.items():
            print(f"Module: {module}")
            evaluations = details.get('evaluations', [])
            for evaluation in evaluations:
                note = evaluation.get('note', {}).get('value', 'N/A')
                description = evaluation.get('description', 'No description')
                print(f"  - {description}: {note}")

if __name__ == "__main__":
    read_notes('data.json')
