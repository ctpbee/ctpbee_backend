from datetime import datetime

from ctpbee import CtpbeeApi
from ctpbee.constant import LogData, AccountData, PositionData


class StrategyClass(CtpbeeApi):
    def __init__(self, name, app=None):
        super().__init__(name, app)

    def on_trade(self, trade):
        pass

    def on_realtime(self):
        self.info("HELLO")

    def on_contract(self, contract):
        pass

    def on_order(self, order):
        pass

    def on_position(self, position: PositionData) -> None:
        pass

    def on_account(self, account: AccountData) -> None:
        """ """
        # print(self.converter.account_df)

    def on_init(self, init):
        pass

    def on_tick(self, tick):
        """tick process function"""

    def on_bar(self, bar):
        """bar process function"""

ext = StrategyClass('LWSB')



