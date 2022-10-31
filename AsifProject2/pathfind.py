import curses  #curses kitabxanası mətn əsaslı terminallar üçün terminaldan müstəqil ekran rəngləmə və klaviatura ilə işləmə qurğusu təqdim edir. Ekran terminalları kursoru hərəkət etdirmək, ekranı sürüşdürmək və sahələri silmək kimi ümumi əməliyyatları yerinə yetirmək üçün müxtəlif idarəetmə kodlarını dəstəkləyir.  
from curses import wrapper #wrapperde cursesi işə salmaq üçün istifadə edilir və sonra proqramı bitirən kimi o, terminalı əvvəlki vəziyyətinə qaytarir.
import queue #biz obyektlərin növbəsini yaratmaq üçün queue modulundan istifadə edirik
import time #adından da göründüyü kimi Python time modulu Python-da vaxtla işləməyə imkan verir. O, cari vaxtı əldə etmək, Proqramın icrasını dayandırmaq kimi funksiyalara imkan verir.

# " "- yolumuz, '*'lavbirintin divarlari, S-start, A-finis
maze = [
    ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],
    ["S", " ", " ", " ", " ", " ", " ", " ", "*", " ", " ", "*", " ", " ", "*"],
    ["*", " ", "*", "*", " ", "*", "*", " ", " ", "*", " ", " ", " ", "*", "*"],
    ["*", " ", "*", " ", " ", " ", "*", " ", "*", " ", " ", " ", "*", " ", "*"],
    ["*", " ", "*", " ", "*", " ", "*", " ", "*", " ", "*", " ", "*", " ", "*"],
    ["*", " ", "*", " ", "*", " ", "*", " ", " ", "*", "*", " ", " ", " ", "*"],
    ["*", " ", "*", " ", "*", " ", "*", "*", " ", " ", "*", " ", "*", " ", "*"],
    ["*", " ", " ", " ", " ", " ", "*", " ", "*", " ", " ", " ", "*", " ", "*"],
    ["*", "*", "*", " ", " ", " ", " ", " ", " ", "*", "*", " ", " ", " ", "*"],
    ["*", " ", "*", "*", " ", "*", "*", " ", "*", "*", "*", "*", "*", " ", "*"],
    ["*", " ", " ", " ", " ", " ", "*", " ", "*", " ", " ", " ", "*", " ", "*"],
    ["*", " ", "*", " ", "*", " ", "*", " ", " ", " ", "*", " ", "*", " ", "*"],
    ["*", " ", " ", " ", "*", " ", "*", " ", "*", "*", " ", " ", " ", " ", "A"],
    ["*", " ", "*", " ", "*", " ", "*", " ", " ", "*", "*", " ", "*", "*", "*"],
    ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"]
]

# labirinti print funksiyasi
def print_maze(maze, stdscr, path=[]): #funksiyanin parametrleri
    #labirintimizin rengleri
    GREEN = curses.color_pair(1) #curses.color(1)-ı GREEN degiskenine atayiriq. 1 yasilin id-si
    MAGENTA = curses.color_pair(2) #curses.color_pair(2)-ı MAGENTA degiskenine atayiriq. 2 magentanin id-si

    for i, row in enumerate(maze): # Enumerate() funksiyasından istifadə etdiyiniz zaman funksiya sizə mazedeki iki döngə dəyişənini geri qaytarır.i ve row
        for j, value in enumerate(row): #bu hissede j columnu temsil edir (i-row,j-column koordinat) Enumerate() funksiyasından istifadə etdiyiniz zaman funksiya sizə rowdaki iki döngə dəyişənini geri qaytarır.j ve value
            if (i, j) in path: #eger i,j path-in daxilindedirse
                stdscr.addstr(i, j*2, "A", MAGENTA) # i,j row ve column. j*2- columnu arali print edir. MAGENTA  A-nin rengi. A hemde bizim current pathimizi temsil edir
            else:
                stdscr.addstr(i, j*2, value, GREEN) #i,j row ve column. j*2- columnu arali print edir.Green *-nin rengi

#find_start funksiyasi
def find_start(maze, start): 
    for i, row in enumerate(maze):  #Enumerate() funksiyasından istifadə etdiyiniz zaman funksiya sizə iki döngə dəyişənini geri qaytarır.i ve row 
        for j, value in enumerate(row):#bu hissede j columnu temsil edir (i-row,j-column koordinat) Enumerate() funksiyasından istifadə etdiyiniz zaman funksiya sizə rowdaki iki döngə dəyişənini geri qaytarır.j ve value
            if value == start: # value S-e beraber olarsa
                return i, j # S-i tapdigi koordinati qaytarir

    return None # S tapilmazsa None
  
#find_path funksiyasi
def find_path(maze, stdscr): 
    #start ve end pozisiyalari
    start = "S" #S-si start-a atayiriq
    end = "A" #A-i end-e atayiriq
    start_pos = find_start(maze, start) #S-in koordinatlarini start_pos-a atayir ve find_start funksiyasini cagir

    q = queue.Queue() #.Queue()- queue modulunun tətbiq üsuludur. Bu moduldan istifade etmek ucun q-e atayiriq
    q.put((start_pos, [start_pos])) #put() metodu Queue nümunəsi ilə təmsil olunan növbəyə element əlavə edir

    visited = set() #ziyarət etdiyimiz bütün mövqeləri özündə birlesdiren ziyarət edilmiş dəst yaradir

    while not q.empty(): #empty() metodu Queue instansiyasında hər hansı elementin olub-olmadığını yoxlayır. Növbədə heç bir element olmadıqda True qaytarır. Əks halda False qaytarır
        current_pos, path = q.get() #get() metodu müəyyən edilmiş açarla elementin dəyərini qaytarır.
        row, col = current_pos #current positionu 2 hisseye yeni row ve columna atayiriq

        stdscr.clear()  #ekranı təmizləyir
        print_maze(maze, stdscr, path) #print_maze funksiyasini cagir
        time.sleep(0.2) #yolu nece tapdigini gormek ucun yavasladiriq
        stdscr.refresh() #ekrani yenileyir

        if maze[row][col] == end: #eger bu mövqe F-ə bərabərdirsə, o deməkdir ki, biz F-i tapmışıq.(shortest path)
            return path # path-i qaytarir
        neighbors = find_neighbors(maze, row, col) #find_neighbors funksiyasini cagirir ve neigborsa atayiriq
        for neighbor in neighbors: #for ile neighbors listindeki her bir elemente catiriq ve neighbora kopyaliyir
            if neighbor in visited: #eger neighbor ziyaret etdiyimiz yerlerin daxilindedirse
                continue 

            r, c = neighbor  #r,c-row,column neighbor-u 2 hisseye row ve columna atayiriq
            if maze[r][c] == "*": #eger maze-de r,c * isaresine beraber olarsa 
                continue 

            new_path = path + [neighbor] #neighboru listin icinde yazilir.path ozu listdi ve 2 listi toplayiriq
            q.put((neighbor, new_path)) #put() metodu Queue nümunəsi ilə təmsil olunan növbəyə element əlavə edir.
            visited.add(neighbor) #add() metodu visited-e neighbor-u əlavə edir.yeni verilmiş elementi çoxluğa əlavə edir 

#qonsulari tapmaq ucun funksiya
def find_neighbors(maze, row, col):
    neighbors = [] #neighbors adinda list yaradiriq

    if row > 0:  # UP eger row>0 olarsa
        neighbors.append((row - 1, col)) #bu zaman neighbors siyahisina row-un -1  veziyyeti ve column liste elave olunur
    if row + 1 < len(maze):  # DOWN  eger row + 1 < len(maze) olarsa
        neighbors.append((row + 1, col)) #bu zaman rowdan +1 veziyyet ve column liste elave olunur
    if col > 0:  # LEFT eger col > 0 olarsa
        neighbors.append((row, col - 1))# row, columndan -1  veziyyet liste elave olunur
    if col + 1 < len(maze[0]):  # RIGHT maze[0]-maze mütləq kvadrat ola bilməz ona gore bele yaziriq
        neighbors.append((row, col + 1)) #row, columndan +1  veziyyet liste elave olunur

    return neighbors #neighbors qaytarir

#esas funksiya
def main(stdscr):
    #labirinti rengleme
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #init_pair(n, f, b)  n-ID(1) f-'*'- nin rengi(yasil) b-arxaplan rengi(qara)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK) #init_pair(n, f, b)  n-ID(1) f-'A'-nin rengi(magenta) b-arxaplan rengi(qara)

    find_path(maze, stdscr) #find_path funksiyasini cagir
    stdscr.getch() #get ch yeni karakter al. input statemente oxsayir.programdan cixmazdan evvel  nese daxil etmeyi gozleyir


wrapper(main) # wrapper funksiyasini cagir