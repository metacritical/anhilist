# Ahilist

MAL to anilist xml exporter.

# MAL to AniList Converter

A simple utility that converts custom or non-standard MyAnimeList XML exports to a format compatible with AniList's import system.

## Description

This tool transforms XML anime list files into the standard MyAnimeList format that AniList accepts for importing. It preserves anime titles, status categories (watching, completed, plan to watch, etc.), and MAL IDs for proper matching during import.

## Features

- Converts custom XML anime list exports to standard MAL format
- Preserves watch status information
- Maintains anime titles and identifiers
- Simple command-line interface

## Requirements

- Ruby
- Nokogiri gem (`gem install nokogiri`)

## Usage

```bash
ruby convert_to_mal.rb INPUT_FILE [-o OUTPUT_FILE]
```

### Arguments

- `INPUT_FILE`: Path to your input XML file
- `-o, --output OUTPUT_FILE`: (Optional) Custom output filename (default: "myanimelist_export.xml")

### Example

```bash
ruby convert_to_mal.rb hianime_mal_export_list.xml -o my_anilist_import.xml
```

## XML Format Support

The script expects input XML with the following structure:

```xml
<list>
  <folder>
    <name>Plan to watch</name>
    <data>
      <item>
        <name>Anime Title</name>
        <link>https://myanimelist.net/anime/12345</link>
      </item>
      <!-- More items... -->
    </data>
  </folder>
  <!-- More folders (Watching, Completed, etc.)... -->
</list>
```

And converts it to AniList-compatible format:

```xml
<myanimelist>
  <anime>
    <series_animedb_id>12345</series_animedb_id>
    <series_title>Anime Title</series_title>
    <my_status>6</my_status>
    <!-- Other required fields... -->
  </anime>
  <!-- More anime entries... -->
</myanimelist>
```

## License

MIT

