import xml.etree.ElementTree as ET

try:
    tree = ET.parse('tmp/wte2.save/data-file-schema.xml')
    root = tree.getroot()

    # Find atomic structure in output (usually under <output> if typical, or root if schema)
    # The grep showed <atomic_positions>... so it's likely just searching explicitly works.
    # Namespace handling might be annoying, so let's iterate.

    atom_lines = []
    cell_lines = []

    # Depending on QE version, structure path varies. 
    # Usually output/atomic_structure
    
    structure = root.find('.//atomic_structure')
    if structure is None:
        # Try finding directly
        print("Could not find atomic_structure block")
        exit(1)

    # Extract Cell
    cell = structure.find('cell')
    for tag in ['a1', 'a2', 'a3']:
        vec = cell.find(tag).text.strip()
        cell_lines.append(vec)

    # Extract Atoms
    positions = structure.find('atomic_positions')
    for atom in positions.findall('atom'):
        name = atom.get('name')
        coords = atom.text.strip()
        atom_lines.append(f"{name} {coords}")

    # Write to file
    with open('new_coords.txt', 'w') as f:
        f.write("CELL_PARAMETERS (bohr)\n")
        f.write("\n".join(cell_lines) + "\n")
        f.write("ATOMIC_POSITIONS (bohr)\n")
        f.write("\n".join(atom_lines) + "\n")

    print("Extraction successful.")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
