import pymongo
from pymongo import MongoClient
import pandas
from optparse import OptionParser
from bson import BSON
from bson import json_util
# import uuid
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="clean from file", metavar="FILE")
parser.add_option("-d", "--database",
                  dest="database",
                  help="clean dat from database in mongodb", metavar="DBNAME")
parser.add_option('-o', '--output',dest="output", action="append", help='specify the output file.  The default is csv')
parser.add_option('-c', '--collection',dest="collection", action="append", help='specify collection from mongodb')

(options, args) = parser.parse_args()

_file = None
if options.filename:
	_file = pandas.read_csv(options.filename)['content']
	_file.index.name = 'id'
elif options.database:
	client = MongoClient('mongodb://localhost:27017/')
	try:
		db = client[str(options.database)]
		_doc = db[''.join(options.collection)]
		_file = pandas.read_json(json_util.dumps(_doc.find()))
	except:
		print 'error, please specify database name and collection name that have in mongodb'
if not _file.empty:
	_file.to_csv(''.join(options.output), encoding='utf-8')







