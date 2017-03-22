from tornado.web import Application, RequestHandler
from tornado.gen import coroutine, sleep
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line, define, options
from tornado.httpserver import HTTPServer
import requests
from pymongo import MongoClient

db = MongoClient("localhost", 27017)['githubleaderboard']
#db = MongoClient("mongodb://apuayush:qwerty1234@ds137110.mlab.com:37110/githubleaderboard")['githubleaderboard']

define("port", default=9125, help="run on the given port", type=int)
# os.environ.get()

class UpdateWeeklyScore(RequestHandler):
    @coroutine
    def get(self):
        while True:
            d = dict()
            projects_name = []
            for projects in requests.get("https://api.github.com/orgs/GDGVIT/repos?client_id=e63b429174efcee3f453&client_secret=baf28b3b72e252c8d54180bfa0b9706e90caa33c").json():
                projects_name.append(
                    [projects['contributors_url'], projects['stargazers_count'], projects['watchers_count'],
                     projects['forks_count'], projects['open_issues']])
            payload={'client_id':'e63b429174efcee3f453','client_secret':'baf28b3b72e252c8d54180bfa0b9706e90caa33c'}
            for i in projects_name:
                for contributors in requests.get(i[0],params=payload).json():

                    """initializing a dictionary member with value as zero for a future new member"""
                    if contributors['login'] not in d.keys():
                        d[contributors['login']] = 0

                    d[contributors['login']] += i[1] * 10 + i[2] * 5 + i[3] * 15 + i[4] * 10 + contributors['contributions'] * 40
            """
            for i in projects_name:
                for contributors in requests.get(i[0], params=payload).json():
                    if(db[contributors['login']].find_one()==None):
                        db[contributors['login']].update({'username': contributors['login']},
                                                         {"$set": {'score': 0,'username':contributors['login']}}, upsert=True)
                    db[contributors['login']].update({'username': contributors['login']},
                                                     {"$set": {'score': d[contributors['login']]-db[contributors['login']].find_one()['score']}}, upsert=True)
                    d[contributors['login']]=0
            """
            for members in d.keys():
                if db[members].find_one() == None:
                    db[members].update({'username': members},
                                                     {"$set": {'score': 0, 'username': members}},
                                                     upsert=True)
                db[members].update({'username': members},
                                                 {"$set": {'score': d[members] -
                                                    db[members].find_one()['score']}},
                                                 upsert=True)
                d[members] = 0

            yield sleep(7 * 24 * 60 * 60)


if __name__ == "__main__":
    parse_command_line()
    app = Application(handlers=[(r'/', UpdateWeeklyScore)], db=db, debug=True)
    server = HTTPServer(app)
    server.listen(options.port)
    IOLoop.instance().start()
