from bs4 import BeautifulSoup
import re
import urllib.parse

from lib.modules.Get import Get



class Webscrape():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    def library_subpage(self,
                        soup: BeautifulSoup,
                        artist_for_url: str,
                        type_flag: str) -> tuple[str, str, str, list[str], str, str]: # type_flag can be "artist", "album" or "track"
        """Manages depending on the type_flag what data to webscrape and returns the data
           type in all contextes here means either artist, album or track, depending on the flag"""

        type_name = ""
        artist_name = ""
        cover_image_url = ""
        metadata_list = [""]
        album_output = ""
        track_output = ""

        if type_flag: # artists/album/track
            type_name = self.type_name(soup, type_flag)

        if any(i == type_flag for i in ["album", "track"]): # album/track
            artist_name = self.artist_name(soup)

        if type_flag: # artists/album/track
            cover_image_url = self.type_image(soup, type_flag)

        if type_flag: # artists/album/track
            metadata_list = self.type_metadata(soup)

        if any(i == type_flag for i in ["artist", "album"]): # artist/album
            track_output, album_output = self.output_lists(soup, artist_for_url, type_flag)

        return type_name, artist_name, cover_image_url, metadata_list, track_output, album_output

    ####################################################################################################

    @staticmethod
    def type_name(soup: BeautifulSoup, type_flag: str) -> str:
        """Webscrapes the artist/album/track name"""

        if not type_flag == "track":
            type_name: str = str(soup.find("h2", class_="library-header-title").text) # Name of the artist/album/track
        else:
            found_type_name = str(soup.find("h2", class_="library-header-title"))
            found_type_name_list = found_type_name.split("<span class=")
            type_name: list[str] = found_type_name_list[0].split('<h2 class="library-header-title">')
            type_name: str = type_name[1].replace("</h2>", "")
            type_name = re.sub('\n', '', type_name.strip())

        return Get().markdown_safe(type_name)

    ####################################################################################################

    @staticmethod
    def artist_name(soup: BeautifulSoup) -> str:
        """Webscrapes the artist/album/track name"""

        artist_name = str(soup.find("a", class_="text-colour-link").text)

        return Get().markdown_safe(artist_name)

    ####################################################################################################

    @staticmethod
    def type_image(soup: BeautifulSoup, type_flag: str) -> str:
        """Webscrapes the artist/album/track cover"""

        if not type_flag == "track":
            found_image = soup.find("span", class_="library-header-image")
            cover_image_url: str = str(found_image.img["src"]) # URL for Artist image or album cover
        else:
            found_image = soup.find("div", class_="library-header-image library-header-image--playlink")
            cover_image_url: str = str(found_image.span.img["src"]) # URL track cover

        return cover_image_url

    ####################################################################################################

    @staticmethod
    def type_metadata(soup: BeautifulSoup) -> list[str]:
        """Webscrapes the total amount of scrobbles/albums/tracks"""

        found_metadata = soup.find_all("p", class_="metadata-display")
        metadata_list = [str(metadata.text) for metadata in found_metadata] # (Scrobbles, Albums, Tracks) for artist | (Scrobbles) for album/track

        return metadata_list # has 3 elements for artist, otherwise 1

    ####################################################################################################

    @staticmethod
    def type_element_positions(soup: BeautifulSoup) -> list[str]:
        """Webscrapes the album/track positions"""

        found_positions = soup.find_all("td", class_="chartlist-index")
        positions_list = [str(position.text).replace(" ", "").replace("\n", "") for position in found_positions]

        return positions_list

    ####################################################################################################

    @staticmethod
    def type_list(soup: BeautifulSoup) -> tuple[list[str], list[str]]:
        """Webscrapes the album/track names and scrobbles"""

        found_names = soup.find_all("td", class_="chartlist-name")
        names_list = [str(name.text) for name in found_names if str(name.text).replace("\n", "")] # can be a track or an album

        found_scorbbles = soup.find_all("span", class_="chartlist-count-bar-value")
        scorbbles_list = [re.sub(r"[^\d]", "", scrobbles.text) for scrobbles in found_scorbbles]

        return names_list, scorbbles_list

    ####################################################################################################

    def output_lists(self, soup: BeautifulSoup, artist_for_url: str, type_flag: str) -> tuple[str, str]:
        """Formates the positions, album/track names and scrobbles and the URLs for the output"""

        positions_list = self.type_element_positions(soup)
        names_list, scorbbles_list = self.type_list(soup)

        album_output = ""
        track_output = ""
        current_element_album = 0

        for position, name, scrobbles in zip(positions_list, names_list, scorbbles_list):
            if int(position) == 1 and type_flag == "artist":
                current_element_album += 1

            name = re.sub('\n', '', name) # can be both album and track

            safe_name = Get().markdown_safe(name)

            element_name_for_url = urllib.parse.quote_plus(name)


            if int(scrobbles) == 1:
                scrobbles += " play"
            else:
                scrobbles += " plays"


            if current_element_album != 1 or type_flag == "album":
                track_output += f"{position}. "
                track_output += f"[{safe_name}](https://www.last.fm/music/{artist_for_url}/_/{element_name_for_url}/) "
                track_output += f"- *({scrobbles})*\n"
            else:
                album_output += f"{position}. "
                album_output += f"[{safe_name}](https://www.last.fm/music/{artist_for_url}/{element_name_for_url}/) "
                album_output += f"- *({scrobbles})*\n"
        
        return track_output, album_output