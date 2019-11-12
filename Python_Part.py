#python aqui
#
#1 - espera que SC pregunti
#2 - computa valor (comenca senzill)
#3 - retorna valor a SC
#

# https://github.com/johnemajor/pyramidtriangles/blob/519c866e9541b96b7051fe9dbc34c4046531e5b9/osc_serve.py
from collections import defaultdict
import logging
from osc4py3 import as_allthreads as osc
# from osc4py3 import as_eventloop as osc
from osc4py3 import oscbuildparse
from osc4py3 import oscmethod
import time

# https://osc4py3.readthedocs.io/en/latest/userdoc.html#logging-osc-operations
# import logging
# logging.basicConfig(format='%(asctime)s - %(threadName)s ø %(name)s - '
#     '%(levelname)s - %(message)s')
# logger = logging.getLogger("osc")
# logger.setLevel(logging.INFO) #INFO, DEBUG, ERROR
#


THROTTLE_TIME = 0.1  # seconds

def send_test_SC(message="a message"):
    print('send SC')
    msg = oscbuildparse.OSCMessage("/control1", None, message)
    osc.osc_send(msg, "sc_client")
    osc.osc_process()

def autosend():
    # print('autosend')
    msg = oscbuildparse.OSCMessage("/print", None, [12345678])
    osc.osc_send(msg, "autoclient_client")
    osc.osc_process()


def server_test():
    logging.info("Instantiating OSCServer:")

    osc.osc_startup()
    #osc.osc_startup(logger=logger)

    osc.osc_udp_server('127.0.0.1', 12000, "main") #test
    osc.osc_udp_client('127.0.0.1', 57122, "sc_client") #testSC
    osc.osc_udp_client('127.0.0.1', 12000, "autoclient_client") #testauto

    send_test_SC()

    def printing_handler(*args):
        # msg_string = "%s [%s] %s" % (addr, tags, str(stuff))
        logging.info("printing_handler called %s %s ", args[0], args[1])
        # send a reply to the client.
        send_test_SC("receive and returned")


    osc.osc_method("/print", printing_handler, argscheme=oscmethod.OSCARG_ADDRESS + oscmethod.OSCARG_DATAUNPACK)

    logging.info("Starting OSC server. Use ctrl-C to quit.")

    try:
        while True:
            osc.osc_process()
            #time.sleep(0.1)
            # autosend()
    except KeyboardInterrupt:
        logging.info("Closing OSC server")
        osc.osc_terminate()


def create_server(listen_address, queue):
    last_msg = defaultdict(float)

    def handler(addr, tags, data, source):
        print("handler")
        now = time.time()
        sincelast = now - last_msg[addr]

        if sincelast >= THROTTLE_TIME:
            logging.debug("%s [%s] %s", addr, tags, str(data))
            last_msg[addr] = now
            queue.put((addr, data))

    osc.osc_startup()
    osc.osc_udp_server(*listen_address, "main")
    # osc.osc_method("/*", handler, argscheme=oscmethod.OSCARG_ADDRESS + oscmethod.OSCARG_DATAUNPACK)
    osc.osc_method("/*", handler)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
    server_test()
