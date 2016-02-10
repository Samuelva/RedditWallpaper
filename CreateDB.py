import sqlite3
import sys

def main(arg):
	conn = sqlite3.connect("Wallpaper.db")
	c = conn.cursor()

	if arg in ["-r", "r", "recreate"]:
		c.execute("""DROP TABLE wallpapers""")

	c.execute("""CREATE TABLE wallpapers (image text)""")

	conn.commit()
	conn.close()



if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		main("x")