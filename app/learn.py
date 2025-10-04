import os

project_dir = r"C:\Users\dell\Downloads\llm8\MedicalAI-Assistant (copy)\app"
for root, dirs, files in os.walk(project_dir):
    level = root.replace(project_dir, '').count(os.sep)
    indent = ' ' * 4 * level
    # Missing print? Add this:
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")
