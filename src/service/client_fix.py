from datetime import datetime, UTC
import quickfix as fix
import time

__SOH__ = chr(1)


class ClientFix(fix.Application):
    ClOrdID = 0

    def onCreate(self, sessionID: fix.SessionID):
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID: fix.SessionID):
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID: fix.SessionID):
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message: fix.Message, sessionID: fix.SessionID):
        msg: str = message.toString()
        print("(Admin) S >> %s" % msg.replace(__SOH__, "|"))
        return

    def fromAdmin(self, message: fix.Message, sessionID: fix.SessionID):
        msg: str = message.toString()
        print("(Admin) R << %s" % msg.replace(__SOH__, "|"))
        return

    def toApp(self, message: fix.Message, sessionID: fix.SessionID):
        msg: str = message.toString()
        print("(App) S >> %s" % msg.replace(__SOH__, "|"))
        return

    def fromApp(self, message: fix.Message, sessionID: fix.SessionID):
        msg: str = message.toString()
        print("(App) R << %s" % msg.replace(__SOH__, "|"))
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message: fix.Message, sessionID: fix.SessionID):
        """Processing application message here"""
        pass

    def genClOrdID(self):
        """Generate ClOrdID"""
        self.ClOrdID += 1
        return str(self.ClOrdID).zfill(5)

    def put_new_order(self):
        """Request sample new order single"""
        message = fix.Message()
        header: fix.Header = message.getHeader()

        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle)) #39 = D 

        message.setField(fix.ClOrdID(self.genClOrdID())) #11 = Unique Sequence Number
        message.setField(fix.Side(fix.Side_BUY)) #43 = 1 BUY 
        message.setField(fix.Symbol("MSFT")) #55 = MSFT
        message.setField(fix.OrderQty(10000)) #38 = 1000
        message.setField(fix.Price(100))
        message.setField(fix.OrdType(fix.OrdType_LIMIT)) #40=2 Limit Order 
        message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION)) #21 = 3
        message.setField(fix.TimeInForce('0'))
        message.setField(fix.Text("NewOrderSingle"))

        trstime = fix.TransactTime()
        trstime.setString(datetime.now(UTC).strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        message.setField(trstime)

        fix.Session.sendToTarget(message, self.sessionID)

    def run(self):
        """Run"""
        while True:
            option = str(input("Please choose 1 for Put New Order or 2 for Exit!\n"))
            if option == '1':
                self.put_new_order()
                print("Done: Put New Order\n")
                continue
            elif option == '2':
                return
            else:
                print("Valid input is 1 for order, 2 for exit\n")
            time.sleep(2)
