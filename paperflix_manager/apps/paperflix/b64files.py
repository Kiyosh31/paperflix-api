
from json import load as load_json
import sqlite3
import base64
import bz2

#=======================================================================
#=======================================================================
#=======================================================================


class FilesDB:
	
	normalize = lambda self, json: ', '.join([("'"+v+"'" if type(v)==str else str(v)) for k, v in json.items()])
	encode = lambda self, data: base64.b64encode(data)
	decode = lambda self, data: base64.b64decode(data)
	
	def __init__(self):
		
		self.db = 'files.sqlite3'
		self.con = sqlite3.connect(self.db)
		self.cur = self.con.cursor()
		self.json = []
	
	# Utilidades: ======================================================
	
	def base64File(self, id_paper):
		
		file_name = self.getFileById(id_paper)
		file_ = self.bz2Decompress(file_name)
		data = self.encode(file_).decode()
		
		return data
	
	def bz2Compress(self, file_name):
		
		f = open('Papers/Papers/'+file_name, 'rb')
		data = f.read()
		data = bz2.compress(data)
		f.close()
		
		return data
	
	def bz2Decompress(self, file_name):
		
		data = self.getFile(file_name)
		data = bz2.decompress(data)
		
		return data
	
	# Gets: ============================================================
	
	def getJson(self):
		
		f = open('files v1.1.json','r', encoding='utf-8')
		self.json = load_json(f)
		f.close()
	
	def getFileById(self, id_paper):
		
		SQL = 'SELECT file_name FROM Files WHERE id_file={};'.format(id_paper)
		self.cur.execute(SQL)
		file_name = self.cur.fetchone()[0]
		
		return file_name
	
	def getFileName(self):
		
		SQL = 'SELECT file_name FROM Files;'
		self.cur.execute(SQL)
		file_names = [f[0] for f in self.cur.fetchall()]
		
		return file_names
	
	def getFileSize(self, file_name):
		
		SQL = 'SELECT bytes_size FROM Files WHERE file_name="{}";'.format(file_name)
		self.cur.execute(SQL)
		
		bytes_size = self.cur.fetchone()[0]
		
		return bytes_size
	
	def getTableFiles(self, fields, where=''):
		
		if where: where = 'WHERE '+where
		
		SQL  = 'SELECT ' + fields
		SQL += ' FROM Files'
		SQL +=   where   + ';'
		
		self.cur.execute(SQL)
	
	def getFile(self, file_name):
		
		SQL = 'SELECT file FROM Files WHERE file_name="{}";'.format(file_name)
		self.cur.execute(SQL)
		
		file_ = self.cur.fetchone()[0]
		
		return file_
	
	# Creates: =========================================================
	
	def createTable(self, table_name):
		
		SQL1 = '''
		CREATE TABLE IF NOT EXISTS {}
		(
			id_file          INTEGER PRIMARY KEY AUTOINCREMENT,
			id_paper         INTEGER UNSIGNED,
			file             BLOB,
			title            VARCHAR(255)     NOT NULL,
			author           VARCHAR(255)     NOT NULL,
			publication_year DATE             NOT NULL,
			category         VARCHAR(255)     NOT NULL,
			language         VARCHAR(32)      NOT NULL,
			num_pages        INTEGER UNSIGNED NOT NULL,
			file_type        VARCHAR(16)      NOT NULL,
			file_name        VARCHAR(255)     NOT NULL,
			extension        VARCHAR(16)      NOT NULL,
			bytes_size       INTEGER UNSIGNED NOT NULL,
			compression_size INTEGER UNSIGNED,
			percent_compress DECIMAL(5,2),
			created_at       DATETIME,
			updated_at       DATETIME
		);
		'''.format(table_name)
		
		SQL2 = '''
		CREATE TRIGGER IF NOT EXISTS file_update
			AFTER UPDATE On {0}
			BEGIN
				UPDATE {0}
				SET updated_at = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')
				WHERE id_file = NEW.id_file;
			END;
		'''.format(table_name)
		
		try:
			self.cur.execute(SQL1)
			self.cur.execute(SQL2)
			print('\n\t [!] Tabla {} Creada con exito!'.format(table_name))
		except sqlite3.OperationalError:
			print('\n\t [!] Error!')
			print(SQL)
	
	def createDatabase(self):
		
		self.createTable('Files')
		self.insertValuesNotNulls()
		self.insertFiles()
		self.con.commit()
	
	# Updates: =========================================================
	
	def insertValuesNotNulls(self):
		
		self.getJson()
		
		for values in self.json:
			
			values = self.normalize(values)
			
			strftime = "STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')"
			
			SQL = '''
			INSERT INTO Files VALUES (null, null, null, {0}, null, null, {1}, {1});
			'''.format(values, strftime)
			
			self.cur.execute(SQL)
	
	def insertFileValues(self, file_name, file_, c_size, percent_c):
		
		strftime = "STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')"
		
		SQL = '''
		UPDATE Files
		SET
			file = ?,
			compression_size = {1},
			percent_compress = {2}
		WHERE id_file = (SELECT id_file FROM Files WHERE file_name='{0}');
		'''.format(file_name, c_size, percent_c)
		
		self.cur.execute(SQL, [sqlite3.Binary(file_)])
	
	def insertFiles(self):
		
		file_names = self.getFileName()
		
		for file_name in file_names:
			
			compressed_data = self.bz2Compress(file_name)
			c_size     = len(compressed_data)
			bytes_size = self.getFileSize(file_name)
			percent_c  = round( 100-((c_size/bytes_size)*100), 2 )
			
			values = {
				'file_name': file_name,
				'file_':     compressed_data,
				'c_size':    c_size,
				'percent_c': percent_c
			}
			
			self.insertFileValues(**values)
			print('File "{}" add.'.format(file_name))


#files_db = FilesDB()
# ~ files_db.createDatabase()
# ~ b64file = files_db.base64File(1)


