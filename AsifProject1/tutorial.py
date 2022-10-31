import curses #curses kitabxanası mətn əsaslı terminallar üçün terminaldan müstəqil ekran rəngləmə və klaviatura ilə işləmə qurğusu təqdim edir. Ekran terminalları kursoru hərəkət etdirmək, ekranı sürüşdürmək və sahələri silmək kimi ümumi əməliyyatları yerinə yetirmək üçün müxtəlif idarəetmə kodlarını dəstəkləyir.  
from curses import wrapper #wrapperde cursesi işə salmaq üçün istifadə edilir və sonra proqramı bitirən kimi o, terminalı əvvəlki vəziyyətinə qaytarir.
import time #adından da göründüyü kimi Python time modulu Python-da vaxtla işləməyə imkan verir. O, cari vaxtı əldə etmək, Proqramın icrasını dayandırmaq kimi funksiyalara imkan verir.
import random #random modulu təsadüfi ədədlər yaratmağa imkan verir.

# start_screen funksiyasi
def start_screen(stdscr): 
	
	stdscr.clear()# ekrani temizleyir
	stdscr.addstr("Welcome to the Speed Typing Test!") # bu hisse ekrana "Welcome to the Speed Typing Test!" print edir/ print() kimi
	stdscr.addstr("\nPress any key to begin!")# bu hisse ekrana \nPress any key to begin! print edir
	stdscr.refresh()# ekrani yenileyir
	stdscr.getkey()#Userin bir shey yazmasini gozleyir ve derhal programi baglamir

#display_text funksiyasi
	
def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)# target parametri cap olunur
	stdscr.addstr(1, 0, f"WPM: {wpm}") #1.0 position ve wpmi print edir
	for i, char in enumerate(current): # enumerate metodu tekrarlanana saygac elave edir ve onu sadalanan obyekt shekilinde qaytarir. i -index char -character
		correct_char = target[i] # targeti correct_char a store edirik
		color = curses.color_pair(1) # curses.color_pair(1)-ı bir degiskende saxlayiriq
		if char != correct_char: #eger daxil etdiyim element target textideki elemente beraber olmasa reng qirmiziya cevrilir
			color = curses.color_pair(2) #2 qirmizi rengin id si

		stdscr.addstr(0, i, char, color) #char,color print olunur
		

#load_text funksiyasi
def load_text():
	with open("text.txt", "r") as f: #fayli acmaq. "r"-fayli oxumaq məlumatlari əldə etmək. Fayldaki melumatlar f de saxlanilir
		lines = f.readlines() ##.readlines()-faylda her bir linedeki yazilardan ibaret list verir
		return random.choice(lines).strip() #listden random 1 element secir.
#wpm_test funksiyasi
def wpm_test(stdscr):
	target_text = load_text() #load_text funksiyasini cagiririq ve load_text-i target_text-e atayiriq
	current_text = []#current_text adinda list yaradiriq
	wpm = 0 #wpm-in baslangic qiymeti
	start_time = time.time() #.time() dövrdən bəri saniyələrlə vaxtı əks etdirən float dəyər qaytarır
	stdscr.nodelay(True) #userin düyməyə basmasını gözləməyi gecikdirmemek

	while True:
		time_elapsed = max(time.time() - start_time, 1) # current vaxtdan baslangic vaxti cixsaq bize qalan vaxti verir.
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5) #wpm-in tapilma dusturu.round-Eger onluq ededdirse onda round ile yuvarlaqlasdiririq

		stdscr.clear()# ekranı təmizləyir
		display_text(stdscr, target_text, current_text, wpm)# display_text funksiyasini cagir
		stdscr.refresh() # ekrani yenileyir

		if "".join(current_text) == target_text:#join() metodu bütün elementləri iterativ olaraq götürür və onları bir sətirdə birləşdirir.
			stdscr.nodelay(False) #odelay() istifadə etdiyim zaman proqram heç bir şey göstərilmədən terminalda işə salındıqdan dərhal sonra çıxır
			break
        #try except funksiyasından istifadə etməyin səbəbi, kodu yazarkən əvvəlcədən görə bilmədiyiniz şərtlərdən asılı olaraq bəzən düzgün işləyəcək, bəzən isə işləməyəcək kod blokunuz olmasıdır.
		try:
			key = stdscr.getkey()  #stdscr.getkey()-i bir degiskende saxlayiriq or degisken atayiriq..getkey() Userin bir shey yazmasini gozleyir ve derhal programi baglamir
		except:
			continue

		if ord(key) == 27: #eger bizim ordinal valuemiz 27 e beraberdise break edir. ASCII 27 = Esc
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):  #backspace bu ucu ile temsil oluna biler.
			if len(current_text) > 0: #current_textin uzunlugu 0-dan boyuk oldugu muddetce
				current_text.pop() #.pop() dan istifade ederek curren_textde son daxil etdiyimiz elementi silecek
		elif len(current_text) < len(target_text): # curren_text deki elementlerin sayi target_text den cox ola bilmez.
			current_text.append(key) #.append funksiyasi vasitesile liste element saxil edir

# esas funksiyamiz
def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)#1 - id curses.COLOR_GREEN yashil reng(foreground), curses.COLOR_BLACK qara reng background 
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)#2 - id curses.COLOR_RED qirmizi reng(foreground), curses.COLOR_BLACK qara reng background 
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)#3 - id curses.COLOR_WHITE ag reng(foreground), curses.COLOR_BLACK qara reng background 

	start_screen(stdscr) # start_screen funksiyasini cagir
	while True:
		wpm_test(stdscr) # wpm_test funksiyasini cagir
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue...") #bu hisse ekrana "You completed the text! Press any key to continue..." print edir. 2 0 ise yazinin koordinatlaridi(row,column)
		key = stdscr.getkey() #stdscr.getkey()-i bir degiskende saxlayiriq. .getkey()Userin bir shey yazmasini gozleyir ve derhal programi baglamir
		
		if ord(key) == 27: #ASCII 27 = escape
			break

wrapper(main) # wrapper funksiyasini cagir
