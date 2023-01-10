from urllib.parse import quote

class Query(object):
    """
    A class for searches made in Goblin.
    """
    def __init__(self, keywords, dep='', cat='', subcat='', size='', des='', cond='', loc='', minp=0, maxp=20000):
        self._kw = keywords
        self._dep = dep
        if dep == 'womenswear':
            self._catpath = 'womens_' + cat + '.' + subcat
            self._size = 'womens_' + cat + '.' + size
        elif dep == 'menswear':
            self._catpath = cat + '.' + subcat
            self._size = cat + '.' + size
        else:
            self._catpath = ''
            self._size = ''
        self._des = des
        self._cond = cond
        self._loc = loc
        self._min = minp
        self._max = maxp

    def getKeywordsURL(self):
        """
        Returns the given keywords in url format.
        """
        return quote(self._kw)

    def getFiltersURL(self):
        """
        Returns the selected fliters of the query in 
        facetFilters and url format.
        """
        return quote(
            '[["department:' +self._dep+ '"],\
            ["category_path:' +self._catpath+ '"],\
            ["category_size:' +self._size+ '"],\
            ["designers.name:' +self._des+ '"],\
            ["condition:' +self._cond+ '"],\
            ["location:' +self._loc+ '"]]')

    def getRangeURL(self):
        """
        Returns the given price range in numericFilters
        and url format.
        """
        return quote('["price_i>=' +str(self._min)+ '","price_i<=' +str(self._max)+ '"]')

    def getKeywordsDB(self):
        """
        Returns keywords in database-compatible format.

        A database-compatible format replaces all spaces with hyphens.
        """
        return self._kw.replace(' ', '_')
