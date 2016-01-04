from pysensu.api import SensuAPI


if __name__ == '__main__':
    sensu = SensuAPI('http://to-rms.sangoma.com:4567')
    print "List of clients connected in sensu: \n"
    print sensu.get_clients()
    print "Info of the client lanner-dev\n"
    print sensu.get_client_data('lanner-dev')
    print "History of the client lanner-dev\n"
    print sensu.get_client_history('lanner-dev')
