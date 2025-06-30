#!/usr/bin/env python3
"""
Schematic diagram generator for the plasmid design.
Creates ASCII-based visual representations of the plasmid structure.
"""

import math
from plasmid_builder import PlasmidDesigner


class PlasmidSchematicGenerator:
    """Generates schematic diagrams of the plasmid."""
    
    def __init__(self, designer: PlasmidDesigner):
        self.designer = designer
        self.width = 80  # Console width for diagrams
    
    def generate_linear_map(self) -> str:
        """Generate a linear representation of the plasmid."""
        linear_map = "\n" + "="*self.width + "\n"
        linear_map += "LINEAR PLASMID MAP (5' to 3')\n"
        linear_map += "="*self.width + "\n\n"
        
        # Create a scaled representation
        scale_factor = (self.width - 10) / self.designer.total_length
        
        # Draw the components
        for i, comp in enumerate(self.designer.components):
            start_pos = int(comp.start_pos * scale_factor)
            end_pos = int(comp.end_pos * scale_factor)
            length = max(1, end_pos - start_pos)
            
            # Component line
            line = " " * start_pos + "█" * length
            line += " " * (self.width - len(line))
            linear_map += f"{line[:self.width]}\n"
            
            # Label
            label = f"{comp.name} ({comp.start_pos}-{comp.end_pos})"
            label_line = " " * start_pos + label
            linear_map += f"{label_line[:self.width]}\n\n"
        
        # Add scale
        linear_map += "\nScale: 1 character ≈ {:.1f} bp\n".format(1/scale_factor)
        linear_map += f"Total length: {self.designer.total_length} bp\n"
        
        return linear_map
    
    def generate_circular_map(self) -> str:
        """Generate a circular representation of the plasmid."""
        circular_map = "\n" + "="*self.width + "\n"
        circular_map += "CIRCULAR PLASMID MAP\n"
        circular_map += "="*self.width + "\n\n"
        
        # Simple circular representation using ASCII
        radius = 15
        center_x, center_y = 25, 15
        
        # Create a grid
        grid = [[' ' for _ in range(50)] for _ in range(30)]
        
        # Draw the circle
        for angle in range(0, 360, 5):
            x = int(center_x + radius * math.cos(math.radians(angle)))
            y = int(center_y + radius * math.sin(math.radians(angle)))
            if 0 <= x < 50 and 0 <= y < 30:
                grid[y][x] = '●'
        
        # Add component markers
        total_angle = 360
        for comp in self.designer.components:
            # Calculate position on circle
            start_angle = (comp.start_pos / self.designer.total_length) * total_angle
            mid_angle = ((comp.start_pos + comp.end_pos) / 2 / self.designer.total_length) * total_angle
            
            # Mark position
            x = int(center_x + (radius + 2) * math.cos(math.radians(mid_angle)))
            y = int(center_y + (radius + 2) * math.sin(math.radians(mid_angle)))
            
            if 0 <= x < 50 and 0 <= y < 30:
                grid[y][x] = comp.name[0]  # First letter of component name
        
        # Convert grid to string
        for row in grid:
            circular_map += ''.join(row) + '\n'
        
        # Add legend
        circular_map += "\nLegend:\n"
        for comp in self.designer.components:
            circular_map += f"  {comp.name[0]} = {comp.name}\n"
        
        circular_map += f"\nTotal plasmid size: {self.designer.total_length} bp\n"
        
        return circular_map
    
    def generate_functional_diagram(self) -> str:
        """Generate a functional flow diagram."""
        diagram = "\n" + "="*self.width + "\n"
        diagram += "FUNCTIONAL FLOW DIAGRAM\n"
        diagram += "="*self.width + "\n\n"
        
        # Transcription flow
        diagram += "TRANSCRIPTION UNIT:\n"
        diagram += "┌─────────────┐    ┌──────────┐    ┌─────────────┐\n"
        diagram += "│ CMV Promoter│ -> │ Neoantigen│ -> │ BGH polyA  │\n"
        diagram += "│   (Strong)  │    │     X     │    │(Terminator)│\n"
        diagram += "└─────────────┘    └──────────┘    └─────────────┘\n\n"
        
        # Translation components
        diagram += "TRANSLATION OPTIMIZATION:\n"
        diagram += "┌─────────────┐    ┌──────────────┐    ┌─────────────┐\n"
        diagram += "│Kozak Sequence│ -> │Signal Peptide│ -> │Neoantigen X │\n"
        diagram += "│ (Ribosome   │    │   (ER Target)│    │  (Optimized)│\n"
        diagram += "│  Binding)   │    │              │    │             │\n"
        diagram += "└─────────────┘    └──────────────┘    └─────────────┘\n"
        diagram += "                                             │\n"
        diagram += "                                             v\n"
        diagram += "                                    ┌─────────────┐\n"
        diagram += "                                    │Expression   │\n"
        diagram += "                                    │Tags (His+   │\n"
        diagram += "                                    │FLAG)        │\n"
        diagram += "                                    └─────────────┘\n\n"
        
        # Plasmid maintenance
        diagram += "PLASMID MAINTENANCE:\n"
        diagram += "┌─────────────┐              ┌─────────────┐\n"
        diagram += "│ColE1 Origin │              │ Ampicillin  │\n"
        diagram += "│(Replication)│              │ Resistance  │\n"
        diagram += "│             │              │ (Selection) │\n"
        diagram += "└─────────────┘              └─────────────┘\n\n"
        
        # mRNA vaccine workflow
        diagram += "mRNA VACCINE WORKFLOW:\n"
        diagram += "Plasmid -> In Vitro Transcription -> mRNA -> Delivery -> Expression\n"
        diagram += "   │              │                    │         │           │\n"
        diagram += "Template     T7/SP6 Polymerase    Capping   Formulation  Immunization\n\n"
        
        return diagram
    
    def generate_sequence_features(self) -> str:
        """Generate detailed sequence feature annotation."""
        features = "\n" + "="*self.width + "\n"
        features += "SEQUENCE FEATURES ANNOTATION\n"
        features += "="*self.width + "\n\n"
        
        for i, comp in enumerate(self.designer.components, 1):
            features += f"{i}. {comp.name}\n"
            features += f"   Position: {comp.start_pos}-{comp.end_pos} ({len(comp.sequence)} bp)\n"
            features += f"   Type: {comp.feature_type}\n"
            features += f"   Description: {comp.description}\n"
            
            # Show first 60 characters of sequence
            seq_preview = comp.sequence[:60]
            if len(comp.sequence) > 60:
                seq_preview += "..."
            features += f"   Sequence: {seq_preview}\n\n"
        
        return features
    
    def generate_complete_schematic(self) -> str:
        """Generate a complete schematic document."""
        complete = "PLASMID pNeoantigenX-mRNA - COMPLETE SCHEMATIC DIAGRAMS\n"
        complete += "="*self.width + "\n"
        
        complete += self.generate_linear_map()
        complete += self.generate_circular_map()
        complete += self.generate_functional_diagram()
        complete += self.generate_sequence_features()
        
        return complete


def main():
    """Generate and display plasmid schematics."""
    print("Generating plasmid schematic diagrams...")
    
    # Create designer and design the plasmid
    designer = PlasmidDesigner()
    designer.design_vector()
    
    # Generate schematics
    schematic_generator = PlasmidSchematicGenerator(designer)
    
    # Display complete schematic
    complete_schematic = schematic_generator.generate_complete_schematic()
    print(complete_schematic)
    
    # Save to file
    with open("plasmid_schematics.txt", "w") as f:
        f.write(complete_schematic)
    
    print("\nSchematic diagrams saved to 'plasmid_schematics.txt'")


if __name__ == "__main__":
    main()