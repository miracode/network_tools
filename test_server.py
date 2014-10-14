
import echo_server

def test_recieve():
    received_msg = echo_server.receive()
    assert received_msg =="message"
