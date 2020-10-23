import sys
import os
import xml.etree.ElementTree as ET

qgis_style_template = """
<!DOCTYPE qgis_style>
<qgis_style version="2">
  <symbols/>
  <colorramps>
    <colorramp type="gradient" name="CustomTest">
       <prop v="255,251,239,255" k="color1"/>
       <prop v="188,184,167,255" k="color2"/>
       <prop v="0" k="discrete"/>
       <prop v="gradient" k="rampType"/>
       <prop v="0.0;255,251,239,255:0.006032;251,251,226,25" k="stops"/>
     </colorramp>
  </colorramps>
  <textformats/>
  <labelsettings/>
</qgis_style>"""

def colormoves_xml_to_string(xml_file):
    """ 
    Converts a colormoves xml gradient to a string of all color stops. 
    The string is a repetition of the pattern: "x;r,g,b,a:"
    Where 
        - x is the x-position on the gradient ranging from (0-1)
        - r/g/b are the red, green and blue values (0-255)
        - a is the transparency value
        
    Takes:
        
        xml_file: string, the color moves xml gradient. Assumes that the file is in the same directory as this script.
        
    Returns:
    
        gradient_as_str: string, the colormoves gradient converted to string format
        
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    gradient_as_str = ""
    for Point in root.iter('Point'):
        x = round(float(Point.get('x')),6)
        o = Point.get('o')
        r = int(float(Point.get('r'))*255)
        g = int(float(Point.get('g'))*255)
        b = int(float(Point.get('b'))*255)
        a = int(float(o)*255)
        gradient_as_str += f"{x};{r},{g},{b},{a}:"
    return gradient_as_str
    
def main(xml_file):
    """
    Converts a colormoves xml gradient to a qgis-compatible xml gradient
    
    Takes:
    
        xml_file: string, the color moves xml gradient. Assumes that the file is in the same directory as this script.
        
    Returns
        
        Nothing. Writes an xml file that can be imported as a style into QGIS
        Output written to working directory. Output name = inputname + "_qgis" 
        
    """
    template_root = ET.fromstring(qgis_style_template)
    gradient_string = colormoves_xml_to_string(xml_file)[:-1] # get gradient string and remove final ":"
    first_color = gradient_string.split(':')[0].split(';')[-1] # get first element and remove x position
    last_color = gradient_string.split(':')[-1].split(';')[-1] # get last eleent and remove x position
    
    for prop in template_root[1][0].findall('prop'):
        key = prop.get('k')
        if key == 'stops':
            prop.set('v',gradient_string)
        elif key == 'color1':
            prop.set('v',first_color)
        elif key == 'color2':
            prop.set('v',last_color)
            
    ramp_name = os.path.splitext(xml_file)[0]
    template_root[1][0].set('name', ramp_name)
    
    output_tree = ET.ElementTree(template_root)
    output_tree.write(f"{ramp_name}_qgis.xml")
    
if __name__ == "__main__":
    xml_file = sys.argv[1]
    main(xml_file)