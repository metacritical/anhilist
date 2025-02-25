import xml.etree.ElementTree as ET
import re
import argparse

def create_anilist_compatible_xml(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    myanimelist = ET.Element("myanimelist")
    
    for folder in root.findall('.//folder'):
        folder_name = folder.find('name').text
        
        for item in folder.find('data').findall('item'):
            name = item.find('name').text
            link = item.find('link').text
            
            mal_id = re.search(r'/anime/(\d+)', link)
            mal_id = mal_id.group(1) if mal_id else "0"
            
            anime = ET.SubElement(myanimelist, "anime")
            
            ET.SubElement(anime, "series_animedb_id").text = mal_id
            ET.SubElement(anime, "series_title").text = name
            
            status_map = {
                "Watching": "1",
                "Completed": "2",
                "On-Hold": "3",
                "Dropped": "4",
                "Plan to watch": "6"
            }
            ET.SubElement(anime, "my_status").text = status_map.get(folder_name, "6")
            
            ET.SubElement(anime, "my_score").text = "0"
            ET.SubElement(anime, "my_watched_episodes").text = "0"
            ET.SubElement(anime, "my_start_date").text = "0000-00-00"
            ET.SubElement(anime, "my_finish_date").text = "0000-00-00"
            ET.SubElement(anime, "my_rewatching").text = "0"
            ET.SubElement(anime, "my_rewatching_ep").text = "0"
            ET.SubElement(anime, "update_on_import").text = "1"
    
    tree = ET.ElementTree(myanimelist)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert custom anime list to MAL format for AniList import')
    parser.add_argument('input_file', help='Input XML file')
    parser.add_argument('-o', '--output', help='Output filename', default='myanimelist_export.xml')
    
    args = parser.parse_args()
    
    success = create_anilist_compatible_xml(args.input_file, args.output)
    
    if success:
        print(f"Conversion completed. Output saved to {args.output}")
