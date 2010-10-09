#coding=UTF-8

class ID3v1(object):
    """ Модуль для анализа ID3v1 тегов.
    """
    
    def __init__ (self):
        ## Название композиции.
        self.title = ""
        ## Название исполнителя.
        self.artist = ""
        ## Название альбома.
        self.album = ""
        ## Год издания.
        self.year = ""
        ## Комментарии.
        self.comment = ""
        ## Жанр композиции.
        self.genre = ""
        ## Номер дорожки в альбоме.
        self.track = ""
    
    def GetTag (self, music_file):
        """ Считывает ID3v1 тэг.
            Производится расшифровка считанного тега и проверка наличия расширенного тега.
            
            @param music_file Объект файла, открытого в режиме "r+b"
            @exception IOError Если в файле тег отсутствует.
        """
        music_file.seek(-128, 2)        #128 байт с конца файла
        ID = music_file.read(3)
        
        if ID != b"TAG":
            raise IOError('This file does not have ID3v1 tag.')
        
        self.title = music_file.read(30)
        self.artist = music_file.read(30)
        self.album = music_file.read(30)
        self.year = music_file.read(4)
        self.comment = music_file.read(30)
        genreId = music_file.read(1)

        if self.comment[28] == 0:
            self.track = self.comment[29]
            self.comment = self.comment[:28]
            
        self.genre = self.GetGenreByID(genreId)
        
        # Чтение расширенного тега, если он есть
        music_file.seek(-355, 2)        # 227 байт перед обычным тегом
        ID = music_file.read(4)

        if ID == b"TAG+":
            self.title += music_file.read(60)
            self.artist += music_file.read(60)
            self.album += music_file.read(60)
            ## Скорость трека. Чем больше число тем активнее музыка. 0 = unset, 1 = slow, 2 = medium, 3 = hardcore
            self.speed = music_file.read(1)
            self.genre = music_file.read(30)
            self.startTime = music_file.read(6)
            self.stopTime = music_file.read(6)
            

    def GetGenreByID (self, code):
        """ Возвращает название жанра по его коду в теге.
            @param code Код жанра.
            @return Строка с названием жанра.
        """
        genres = {0 :"Blues",
                  1 :"Classic Rock",
                  2 :"Country",
                  3 :"Dance",
                  4 :"Disco",
                  5 :"Funk",
                  6 :"Grunge",
                  7 :"Hip-Hop",
                  8 :"Jazz",
                  9 :"Metal",
                  10 :"New Age",
                  11 :"Oldies",
                  12 :"Other",
                  13 :"Pop",
                  14 :"R&B",
                  15 :"Rap",
                  16 :"Reggae",
                  17 :"Rock",
                  18 :"Techno",
                  19 :"Industrial",
                  20 :"Alternative",
                  21 :"Ska",
                  22 :"Death Metal",
                  23 :"Pranks",
                  24 :"Soundtrack",
                  25 :"Euro-Techno",
                  26 :"Ambient",
                  27 :"Trip-Hop",
                  28 :"Vocal",
                  29 :"Jazz+Funk",
                  30 :"Fusion",
                  31 :"Trance",
                  32 :"Classical",
                  33 :"Instrumental",
                  34 :"Acid",
                  35 :"House",
                  36 :"Game",
                  37 :"Sound Clip",
                  38 :"Gospel",
                  39 :"Noise",
                  40 :"AlternRock",
                  41 :"Bass",
                  42 :"Soul",
                  43 :"Punk",
                  44 :"Space",
                  45 :"Meditative",
                  46 :"Instrumental Pop",
                  47 :"Instrumental Rock",
                  48 :"Ethnic",
                  49 :"Gothic",
                  50 :"Darkwave",
                  51 :"Teckno-Industrial",
                  52 :"Electronic",
                  53 :"Pop-Folk",
                  54 :"Eurodance",
                  55 :"Dream",
                  56 :"Southern Rock",
                  57 :"Comedy",
                  58 :"Cult",
                  59 :"Gangsta",
                  60 :"Top 40",
                  61 :"Christian Rap",
                  62 :"Pop/Funk",
                  63 :"Jungle",
                  64 :"Native American",
                  65 :"Cabaret",
                  66 :"New Wave",
                  67 :"Psychadelic",
                  68 :"Rave",
                  69 :"Showtunes",
                  70 :"Trailer",
                  71 :"Lo-Fi",
                  72 :"Tribal",
                  73 :"Acid Punk",
                  74 :"Acid Jazz",
                  75 :"Polka",
                  76 :"Retro",
                  77 :"Musical",
                  78 :"Rock & Roll",
                  79 :"Hard Rock",
                  80 :"Folk",
                  81 :"Folk-Rock",
                  82 :"National Folk",
                  83 :"Swing",
                  84 :"Fast Fusion",
                  85 :"Bebob",
                  86 :"Latin",
                  87 :"Revival",
                  88 :"Celtic",
                  89 :"Bluegrass",
                  90 :"Avantgarde",
                  91 :"Gothic Rock",
                  92 :"Progessive Rock",
                  93 :"Psychadelic Rock",
                  94 :"Symphonic Rock",
                  95 :"Slow Rock",
                  96 :"Big Band",
                  97 :"Chorus",
                  98 :"Easy Listening",
                  99 :"Acoustic",
                  100 :"Humour",
                  101 :"Speech",
                  102 :"Chanson",
                  103 :"Opera",
                  104 :"Chamber Music",
                  105 :"Sonata",
                  106 :"Symphony",
                  107 :"Booty Brass",
                  108 :"Primus",
                  109 :"Porn Groove",
                  110 :"Satire",
                  111 :"Slow Jam",
                  112 :"Club",
                  113 :"Tango",
                  114 :"Samba",
                  115 :"Folklore",
                  116 :"Ballad",
                  117 :"Poweer Ballad",
                  118 :"Rhytmic Soul",
                  119 :"Freestyle",
                  120 :"Duet",
                  121 :"Punk Rock",
                  122 :"Drum Solo",
                  123 :"A Capela",
                  124 :"Euro-House",
                  125 :"Dance Hall",
                  126 :"Goa",
                  127 :"Drum & Bass",
                  128 :"Club-House",
                  129 :"Hardcore",
                  130 :"Terror",
                  131 :"Indie",
                  132 :"BritPop",
                  133 :"Negerpunk",
                  134 :"Polsk punk",
                  135 :"Beat",
                  136 :"Christian Gangsta",
                  137 :"Heavy Metal",
                  138 :"Black Metal",
                  139 :"Crossover",
                  140 :"Contemporary C",
                  141 :"Christian Rock",
                  142 :"Merengue",
                  143 :"Salsa",
                  144 :"Thrash Metal",
                  145 :"Anime",
                  146 :"JPop",
                  147 :"SynthPop"}
                  
        return genres.get(ord(code), "Unknown")

