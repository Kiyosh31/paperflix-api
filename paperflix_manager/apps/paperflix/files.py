
import sqlite3
import base64
import bz2
import os


#=======================================================================
#=======================================================================
#=======================================================================


class FilesDB:
	
	encode = lambda self, data: base64.b64encode(data)
	decode = lambda self, data: base64.b64decode(data)
	
	def __init__(self):
		
		self.db = 'files.sqlite3'
	
	# Creates: =========================================================

	def createDatabase(self, table_name):
		
		self.con = sqlite3.connect(self.db)
		self.cur = self.con.cursor()

		print(True)
		SQL1 = '''
		CREATE TABLE IF NOT EXISTS {}
		(
			id_file          INTEGER PRIMARY KEY AUTOINCREMENT,
			id_paper         INTEGER UNSIGNED,
			file             BLOB,
			created_at       DATETIME
		);
		'''.format(table_name)
		
		self.cur.execute(SQL1)
		self.con.commit()

		self.cur.close()
		self.con.close()
	
	# Utilidades: ======================================================
	
	def setFile(self, id_paper, file_):
		
		self.con = sqlite3.connect(self.db)
		self.cur = self.con.cursor()
		
		file_ = file_.replace('data:application/pdf;base64,','')
		file_ = self.decode(file_.encode())
		file_ = bz2.compress(file_)
		SQL = 'INSERT INTO Files VALUES (null, ?, ?, ?)'
		data = [
			id_paper,
			sqlite3.Binary(file_),
			"STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')"
		]
		
		self.cur.execute(SQL, data)
		self.con.commit()

		self.cur.close()
		self.con.close()

	def getFile(self, id_paper):
		
		self.con = sqlite3.connect(self.db)
		self.cur = self.con.cursor()
		
		SQL = 'SELECT file FROM Files WHERE id_paper={};'.format(id_paper)
		self.cur.execute(SQL)
		file_ = self.cur.fetchone()[0]
		file_ = bz2.decompress(file_)
		
		self.cur.close()
		self.con.close()
		
		return file_

	def deleteFile(self, id_paper):
		self.con = sqlite3.connect(self.db)
		self.cur = self.con.cursor()

		SQL = 'DELETE FROM Files WHERE id_paper={};'.format(id_paper)
		self.cur.execute(SQL)
		self.con.commit()

		self.cur.close()
		self.con.close()
	
	def getFileb64(self, id_paper):
		
		file_ = self.getFile(id_paper)
		data = self.encode(file_).decode()
		
		return data


files_db = FilesDB()
if not os.path.exists(files_db.db):
	files_db.createDatabase('Files')
