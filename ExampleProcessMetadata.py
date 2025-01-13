import re
import pandas as pd

# Define regex patterns for folder structures
patterns = [
    # Match with photographer/collector and species
    r".*?(?P<ObjectCollector>[a-zA-Z]+).*?(?P<Hash>[a-z0-9]+)__(?P<SpeciesName>[a-zA-Z_]+)__(?P<ViewType>[a-zA-Z_]+)(?:_.*)?",
    # Match general HASH with species and view
    r".*?(?P<Hash>[a-z0-9]+)__(?P<SpeciesName>[a-zA-Z_]+)__(?P<ViewType>[a-zA-Z_]+)(?:_.*)?",
]

# Parse folder metadata
def parse_folder(folder_name, patterns):
    for pattern in patterns:
        match = re.search(pattern, folder_name)
        if match:
            metadata = match.groupdict()
            # Assign default values for missing fields
            metadata.setdefault("ObjectCollector", "Unknown")
            metadata.setdefault("CollectionObject", "Unknown")
            metadata["FolderPath"] = folder_name
            return metadata
    return None

# Example folder list
folder_names = [
    "G:/RawStackBilder/coll.mfn-berlin.de_u_09f74e__Polydesmus_python__ventral_90mm_1zu3",
    "G:/RawStackBilder/DoD-IDN-00099__Jurisch/7a9fc7__Anomala_poecilochalcea/7a9fc7__Anomala_poecilochalcea__dorsal__1x-90mm",
    "G:/RawStackBilder/DoD-IDN-00106__Jurisch/09f4de__Lachnosterna_ferruginea/09f4de__Lachnosterna_ferruginea__genial_dorsal__5x",
    "G:/RawStackBilder/DoD_IDN_00107__Kristina/Rhaconotus_crenulatus__ZMB604_male/Rhaconotus_crenulatus__ZMB604_male__ventral",
    "G:/RawStackBilder/K2_R11_Sp014_Landassel__09edc2__dorsal",
]

# Parse folders
parsed_data = []
for folder in folder_names:
    metadata = parse_folder(folder, patterns)
    if metadata:
        parsed_data.append(metadata)

# Convert to DataFrame
folders_df = pd.DataFrame(parsed_data)

# Save the parsed metadata to CSV
folders_df.to_csv("parsed_folders_metadata.csv", index=False)

# Display results
print("Parsed Folder Metadata:")
print(folders_df)
