import os
import configparser

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class App:

    def __init__(self):
        self.username = '33OsmcVr1W9s'
        self.password = '33OsmcVr1W9s'
        self.home = '/home/jorge/ftp/'
        self.stable = 'stable/'
        self.testing = 'testing/'
        self.address = ('0.0.0.0', 2121)

    def init_dirs(self):
        if not os.path.exists(self.home):
            print('Creating all directories')
            os.mkdir(self.home)
            os.mkdir(''.join([self.home, self.stable]))
            os.mkdir(''.join([self.home, self.testing]))
        elif not os.path.exists(''.join([self.home, self.stable])):
            print('Creating stable directory')
            os.mkdir(''.join([self.home, self.stable]))
        elif not os.path.exists(''.join([self.home, self.testing])):
            print('Creating testing directory')
            os.mkdir(''.join([self.home, self.testing]))

    def init_ftp(self):
        authorizer = DummyAuthorizer()
        authorizer.add_user(username=self.username, password=self.password, homedir=self.home)
        handler = FTPHandler
        handler.authorizer = authorizer
        handler.banner = "Welcome."
        server = FTPServer(address_or_socket=self.address, handler=handler)
        server.max_cons = 256
        server.max_cons_per_ip = 5
        server.serve_forever()

    def load_config(self):
        config = configparser.ConfigParser()
        try:
            config.read(''.join([os.getcwd(), '/config.ini']))
            self.username = config['DEFAULT']['Username']
            self.password = config['DEFAULT']['Password']
            self.home = config['DEFAULT']['FTP_home']
            self.address = (config['DEFAULT']['Listen_address'], int(config['DEFAULT']['Listen_port']))
        except KeyError:
            pass

    def main(self):
        self.load_config()
        self.init_dirs()
        self.init_ftp()


if __name__ == '__main__':
    App().main()
