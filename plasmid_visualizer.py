#!/usr/bin/env python3
"""
Plasmid Visualization Module for mRNA Vaccine Prototype
Creates schematic diagrams of the plasmid vector design.
"""

import json
import math
from typing import Dict, List, Tuple, Optional
from plasmid_builder import PlasmidBuilder, PlasmidElement, ElementType


class PlasmidVisualizer:
    """Creates visual representations of plasmid designs"""
    
    # Color scheme for different element types
    ELEMENT_COLORS = {
        ElementType.PROMOTER: "#FF6B6B",    # Red
        ElementType.GENE: "#4ECDC4",        # Teal
        ElementType.TAG: "#45B7D1",         # Blue
        ElementType.ENHANCER: "#FFA07A",    # Light Salmon
        ElementType.UTR: "#98D8C8",         # Mint
        ElementType.ORIGIN: "#F7DC6F",      # Yellow
        ElementType.RESISTANCE: "#BB8FCE"   # Purple
    }
    
    @classmethod
    def generate_ascii_diagram(cls, builder: PlasmidBuilder) -> str:
        """Generate ASCII art representation of the plasmid"""
        diagram = []
        diagram.append("=" * 80)
        diagram.append(f"PLASMID VECTOR: {builder.name.upper()}")
        diagram.append(f"Total Length: {builder.total_length} bp")
        diagram.append("=" * 80)
        diagram.append("")
        
        # Create a linear map
        diagram.append("LINEAR MAP:")
        diagram.append("-" * 60)
        
        position = 0
        for i, element in enumerate(builder.elements):
            # Calculate relative position for visualization
            bar_length = max(1, int(element.length / builder.total_length * 50))
            bar = "█" * bar_length
            
            diagram.append(f"{position:>5} bp |{bar}| {element.name}")
            diagram.append(f"         {' ' * len(bar)}  Type: {element.element_type.value}")
            diagram.append(f"         {' ' * len(bar)}  Length: {element.length} bp")
            if element.description:
                diagram.append(f"         {' ' * len(bar)}  Desc: {element.description[:40]}...")
            diagram.append("")
            
            position += element.length
        
        diagram.append("-" * 60)
        diagram.append("")
        
        # Create circular representation (simplified)
        diagram.append("CIRCULAR MAP (Simplified):")
        diagram.append("")
        radius = 15
        center_x, center_y = 20, 15
        
        # Create the circular diagram grid
        grid = [[' ' for _ in range(40)] for _ in range(30)]
        
        # Draw the circle
        for angle in range(0, 360, 5):
            x = int(center_x + radius * math.cos(math.radians(angle)))
            y = int(center_y + radius * math.sin(math.radians(angle)))
            if 0 <= x < 40 and 0 <= y < 30:
                grid[y][x] = '●'
        
        # Add element labels around the circle
        cumulative_angle = 0
        for element in builder.elements:
            element_angle = 360 * element.length / builder.total_length
            mid_angle = cumulative_angle + element_angle / 2
            
            # Position label outside the circle
            label_radius = radius + 5
            label_x = int(center_x + label_radius * math.cos(math.radians(mid_angle)))
            label_y = int(center_y + label_radius * math.sin(math.radians(mid_angle)))
            
            # Truncate label if too long
            label = element.name[:8] if len(element.name) > 8 else element.name
            
            # Place label in grid if within bounds
            if 0 <= label_x < 35 and 0 <= label_y < 30:
                for i, char in enumerate(label):
                    if label_x + i < 40:
                        grid[label_y][label_x + i] = char
            
            cumulative_angle += element_angle
        
        # Convert grid to string
        for row in grid:
            diagram.append(''.join(row))
        
        diagram.append("")
        diagram.append("=" * 80)
        
        return '\n'.join(diagram)
    
    @classmethod
    def generate_element_summary(cls, builder: PlasmidBuilder) -> str:
        """Generate a detailed summary of all elements"""
        summary = []
        summary.append("ELEMENT SUMMARY")
        summary.append("=" * 50)
        summary.append("")
        
        # Group elements by type
        elements_by_type = {}
        for element in builder.elements:
            element_type = element.element_type
            if element_type not in elements_by_type:
                elements_by_type[element_type] = []
            elements_by_type[element_type].append(element)
        
        # Display by type
        for element_type, elements in elements_by_type.items():
            summary.append(f"{element_type.value.upper()} ELEMENTS:")
            summary.append("-" * 30)
            
            for element in elements:
                summary.append(f"  • {element.name}")
                summary.append(f"    Position: {element.position}-{element.position + element.length} bp")
                summary.append(f"    Length: {element.length} bp")
                if element.description:
                    summary.append(f"    Description: {element.description}")
                summary.append("")
            
            summary.append("")
        
        return '\n'.join(summary)
    
    @classmethod
    def generate_mrna_transcript_map(cls, builder: PlasmidBuilder) -> str:
        """Generate a map of the mRNA transcript (excluding plasmid maintenance)"""
        mrna_elements = [
            element for element in builder.elements 
            if element.element_type != ElementType.RESISTANCE
        ]
        
        diagram = []
        diagram.append("mRNA TRANSCRIPT MAP")
        diagram.append("=" * 50)
        diagram.append("")
        diagram.append("5' → 3' Direction:")
        diagram.append("")
        
        position = 0
        for element in mrna_elements:
            arrow = "→" if element.element_type == ElementType.GENE else "•"
            diagram.append(f"{position:>4} bp {arrow} {element.name} ({element.length} bp)")
            position += element.length
        
        diagram.append("")
        diagram.append(f"Total mRNA length: {sum(e.length for e in mrna_elements)} bp")
        diagram.append("")
        
        # Show protein coding region specifically
        diagram.append("PROTEIN CODING REGION:")
        diagram.append("-" * 30)
        
        in_coding = False
        for element in mrna_elements:
            if element.name == "Start Codon":
                in_coding = True
                diagram.append(f"  START → {element.name}")
            elif element.name == "Stop Codon":
                diagram.append(f"  STOP → {element.name}")
                in_coding = False
            elif in_coding and element.element_type == ElementType.GENE:
                diagram.append(f"    CODING → {element.name}")
            elif in_coding and element.element_type == ElementType.TAG:
                diagram.append(f"    TAG → {element.name}")
        
        return '\n'.join(diagram)
    
    @classmethod
    def export_svg_diagram(cls, builder: PlasmidBuilder, filename: str = "plasmid_diagram.svg") -> str:
        """Export plasmid as SVG diagram (basic implementation)"""
        width, height = 400, 400
        center_x, center_y = width // 2, height // 2
        radius = 150
        
        svg_content = []
        svg_content.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')
        svg_content.append('<style>')
        svg_content.append('text { font-family: Arial, sans-serif; font-size: 10px; }')
        svg_content.append('.title { font-size: 16px; font-weight: bold; }')
        svg_content.append('</style>')
        
        # Title
        svg_content.append(f'<text x="{center_x}" y="30" text-anchor="middle" class="title">{builder.name}</text>')
        svg_content.append(f'<text x="{center_x}" y="50" text-anchor="middle">Total: {builder.total_length} bp</text>')
        
        # Draw main circle
        svg_content.append(f'<circle cx="{center_x}" cy="{center_y}" r="{radius}" fill="none" stroke="black" stroke-width="2"/>')
        
        # Draw elements as colored arcs
        cumulative_angle = 0
        for element in builder.elements:
            element_angle = 360 * element.length / builder.total_length
            
            # Calculate arc parameters
            start_angle = cumulative_angle
            end_angle = cumulative_angle + element_angle
            
            # Convert to radians for calculations
            start_rad = math.radians(start_angle - 90)  # -90 to start from top
            end_rad = math.radians(end_angle - 90)
            
            # Calculate arc endpoints
            x1 = center_x + radius * math.cos(start_rad)
            y1 = center_y + radius * math.sin(start_rad)
            x2 = center_x + radius * math.cos(end_rad)
            y2 = center_y + radius * math.sin(end_rad)
            
            # Determine if arc is large
            large_arc_flag = 1 if element_angle > 180 else 0
            
            # Get color for element type
            color = cls.ELEMENT_COLORS.get(element.element_type, "#CCCCCC")
            
            # Draw arc
            if element_angle < 360:  # Don't draw full circle
                arc_path = f'M {x1} {y1} A {radius} {radius} 0 {large_arc_flag} 1 {x2} {y2}'
                svg_content.append(f'<path d="{arc_path}" stroke="{color}" stroke-width="8" fill="none"/>')
            
            # Add label
            mid_angle = start_angle + element_angle / 2
            mid_rad = math.radians(mid_angle - 90)
            label_radius = radius + 20
            label_x = center_x + label_radius * math.cos(mid_rad)
            label_y = center_y + label_radius * math.sin(mid_rad)
            
            # Truncate long names
            label_text = element.name[:10] if len(element.name) > 10 else element.name
            svg_content.append(f'<text x="{label_x}" y="{label_y}" text-anchor="middle">{label_text}</text>')
            
            cumulative_angle += element_angle
        
        # Add legend
        legend_y = height - 100
        svg_content.append(f'<text x="20" y="{legend_y - 10}" class="title">Legend:</text>')
        
        y_offset = 0
        for element_type, color in cls.ELEMENT_COLORS.items():
            y_pos = legend_y + y_offset * 15
            svg_content.append(f'<rect x="20" y="{y_pos}" width="12" height="12" fill="{color}"/>')
            svg_content.append(f'<text x="40" y="{y_pos + 10}">{element_type.value.title()}</text>')
            y_offset += 1
        
        svg_content.append('</svg>')
        
        svg_string = '\n'.join(svg_content)
        
        # Write to file
        with open(filename, 'w') as f:
            f.write(svg_string)
        
        return svg_string


def main():
    """Demonstration of plasmid visualization"""
    from plasmid_builder import main as build_plasmid
    
    # Get a plasmid design
    builder, design = build_plasmid()
    
    print("Generating plasmid visualizations...")
    print()
    
    # Generate ASCII diagram
    ascii_diagram = PlasmidVisualizer.generate_ascii_diagram(builder)
    print(ascii_diagram)
    print()
    
    # Generate element summary
    element_summary = PlasmidVisualizer.generate_element_summary(builder)
    print(element_summary)
    print()
    
    # Generate mRNA transcript map
    mrna_map = PlasmidVisualizer.generate_mrna_transcript_map(builder)
    print(mrna_map)
    print()
    
    # Export SVG diagram
    svg_content = PlasmidVisualizer.export_svg_diagram(builder, "neoantigen_x_plasmid.svg")
    print("SVG diagram exported to: neoantigen_x_plasmid.svg")


if __name__ == "__main__":
    main()