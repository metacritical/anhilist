require 'nokogiri'
require 'optparse'

def create_anilist_compatible_xml(input_file, output_file)
  doc = File.open(input_file) { |f| Nokogiri::XML(f) }
  
  builder = Nokogiri::XML::Builder.new(encoding: 'UTF-8') do |xml|
    xml.myanimelist {
      doc.xpath('//folder').each do |folder|
        folder_name = folder.at_xpath('./name').text
        
        folder.xpath('./data/item').each do |item|
          name = item.at_xpath('./name').text
          link = item.at_xpath('./link').text
          
          mal_id = link.match(/\/anime\/(\d+)/)
          mal_id = mal_id ? mal_id[1] : "0"
          
          xml.anime {
            xml.series_animedb_id mal_id
            xml.series_title name
            
            status_map = {
              "Watching" => "1",
              "Completed" => "2",
              "On-Hold" => "3",
              "Dropped" => "4",
              "Plan to watch" => "6"
            }
            xml.my_status status_map[folder_name] || "6"
            
            xml.my_score "0"
            xml.my_watched_episodes "0"
            xml.my_start_date "0000-00-00"
            xml.my_finish_date "0000-00-00"
            xml.my_rewatching "0"
            xml.my_rewatching_ep "0"
            xml.update_on_import "1"
          }
        end
      end
    }
  end
  
  File.write(output_file, builder.to_xml)
  true
end

options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: convert_to_mal.rb INPUT_FILE [options]"
  
  opts.on("-o", "--output FILENAME", "Output filename") do |o|
    options[:output] = o
  end
end.parse!

input_file = ARGV[0]
output_file = options[:output] || "myanimelist_export.xml"

if input_file.nil?
  puts "Error: Input file is required"
  puts "Usage: convert_to_mal.rb INPUT_FILE [-o OUTPUT_FILE]"
  exit 1
end

success = create_anilist_compatible_xml(input_file, output_file)

if success
  puts "Conversion completed. Output saved to #{output_file}"
end
