import quickfix as fix
import time

__SOH__ = chr(1)


class ServerFix(fix.Application):
    orderID = 0
    execID = 0

    def onCreate(self, sessionID: fix.SessionID):
        """onCreate"""
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID: fix.SessionID):
        """onLogon"""
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID: fix.SessionID):
        """onLogout"""
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message: fix.Message, sessionID: fix.SessionID):
        msg: str = message.toString()
        msg = msg.replace(__SOH__, "|")
        print("(Admin) S >> %s" % msg)
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
        """Mockup execution report for newordersingle"""
        beginString = fix.BeginString()
        msgType = fix.MsgType()
        header: fix.Header = message.getHeader()
        header.getField(beginString)
        header.getField(msgType)

        symbol = fix.Symbol()
        side = fix.Side()
        ordType = fix.OrdType()
        orderQty = fix.OrderQty()
        price = fix.Price()
        clOrdID = fix.ClOrdID()

        message.getField(ordType)

        if ordType.getValue() != fix.OrdType_LIMIT:
            raise fix.IncorrectTagValue(ordType.getField())

        message.getField(symbol)
        message.getField(side)
        message.getField(orderQty)
        message.getField(price)
        message.getField(clOrdID)

        executionReport = fix.Message()
        executionReportHeader: fix.Header = executionReport.getHeader()
        executionReportHeader.setField(beginString)
        executionReportHeader.setField(fix.MsgType(fix.MsgType_ExecutionReport))

        executionReport.setField(fix.OrderID(self.genOrderID()))
        executionReport.setField(fix.ExecID(self.genExecID()))
        executionReport.setField(fix.OrdStatus(fix.OrdStatus_FILLED))
        executionReport.setField(symbol)
        executionReport.setField(side)
        executionReport.setField(fix.CumQty(orderQty.getValue()))
        executionReport.setField(fix.AvgPx(price.getValue()))
        executionReport.setField(fix.LastShares(orderQty.getValue()))
        executionReport.setField(fix.LastPx(price.getValue()))
        executionReport.setField(clOrdID)
        executionReport.setField(orderQty)

        if beginString.getValue() in (fix.BeginString_FIX40, fix.BeginString_FIX41,fix.BeginString_FIX42):
            executionReport.setField(fix.ExecTransType(fix.ExecTransType_NEW))

        if beginString.getValue() >= fix.BeginString_FIX41:
            executionReport.setField(fix.ExecType(fix.ExecType_FILL))
            executionReport.setField(fix.LeavesQty(0))

        try:
            fix.Session.sendToTarget(executionReport, sessionID)
        except fix.SessionNotFound as error:
            print(error)
            return

    def genOrderID(self):
        self.orderID += 1
        return str(self.orderID).zfill(5)

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

    def run(self):
        """Run"""
        while True:
            time.sleep(2)
