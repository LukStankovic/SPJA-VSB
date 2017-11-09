import http.client as httplib
import xml.etree.ElementTree as ET


class Error(Exception):
    pass


class CannotRetrieveUrlError(Error):
    def __init__(self, url):
        self.msg = "Cannot retrieve URL: " + url


class FeedItem(object):
    """
    Reprezentuje jeden item ve feedu, tzn.
    <item>
    ...
    </item>
    """
    # TODO 5
    def __init__(self, item):
        self.__title = item[0]
        self.__description = item[1]
        self.__guid = item[2]

    def __str__(self):
        return "Název: " + self.title + ", popis: " + self.description + ", GUID: " + self.guid

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def guid(self):
        return self.__guid

    @guid.setter
    def guid(self, guid):
        self.__guid = guid


class Feed(object):
    """
    Reprezentuje feed, tzn. kanal, ve kterem jsou jednotlive prispevky.
    <channel>
    </channel>
    """

    def __init__(self, feed_xml):
        # tato promenna udrzuje string s XML daty, ktera byla
        # stazena ze serveru. Pouzijte ji pro parsovani XML.
        self.feed_xml = feed_xml

        self.title, self.desc, self.lang = self.parse_feed_info()

    def print_info(self):
        print("=====================")
        print("Feed info:")
        print("Title: {}".format(self.title))
        print("Desc: {}".format(self.desc))
        print("Lang: {}".format(self.lang))
        print("=====================")
        print()

    def parse_feed_info(self):
        # TODO 2:z XML dat vrati trojici obsahujici informace o feedu
        # title, description, language
        for channel in ET.fromstring(self.feed_xml):
            return channel.find('title').text, channel.find('description').text, channel.find('language').text

    def items(self):
        items = []
        for channel in ET.fromstring(self.feed_xml):
            for item in channel:
                if item.tag == 'item':
                    items.append((item.find('title').text, item.find('description').text, item.find('guid').text))

        feed_items = []

        for item in items:
            feed_items.append(FeedItem(item))

        return feed_items
        # TODO 3:z XML dat vrati vsechny itemy, ktere feed obsahuje
        # generujte list tuplu (title, desc, guid)
        # Pro TODO 5 generujte instance tridy FeedItem


class Reader(object):
    """
    Reprezentuje RSS ctecku, ktera umi cist vice RSS feedu.
    Pro jednoduchost budeme pouze cist jeden RSS feed.
    """

    def __init__(self, url):
        self.url = url
        self.feed = None

    def fetch_feed(self):
        conn = httplib.HTTPConnection(self.url)
        conn.request("GET", "/")
        r = conn.getresponse()
        # print type(r.status), type(r.reason)
        if r.status != 200:
            raise CannotRetrieveUrlError(self.url)

        xml = r.read()
        self.feed = Feed(xml)
        self.feed.print_info()
        # TODO 1: doplnit vytvoreni objektu Feed do promenne self.feed
        # pro overeni splneni TODO 2 zde take zavolat metodu feed.print_info()

        conn.close()

    def read_feed(self):
        for item in self.feed.items():
            print(item)

        # TODO 4, X:z feedu precist itemy pomoci funkce feed.items()
        # a vytisknout na obrazovku
        pass


def main():
    url = 'localhost:9000'
    reader = Reader(url)

    try:
        reader.fetch_feed()
        reader.read_feed()
    except CannotRetrieveUrlError as e:
        print(e)


if __name__ == '__main__':
    main()
