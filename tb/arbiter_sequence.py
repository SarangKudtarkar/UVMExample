from pyuvm import uvm_sequence
from tb.arbiter_seq_item import ArbiterSeqItem


class ArbiterBasicSequence(uvm_sequence):

    def __init__(self, name="ArbiterBasicSequence"):
        super().__init__(name)

    async def body(self):

        # Transaction 1: No request
        item = ArbiterSeqItem("item_no_request")
        item.req = 0
        item.data0 = 0x00
        item.data1 = 0x00

        await self.start_item(item)
        await self.finish_item(item)

        # Transaction 2: User 0
        item = ArbiterSeqItem("item_user0")
        item.req = 1
        item.data0 = 0xAA
        item.data1 = 0x55

        await self.start_item(item)
        await self.finish_item(item)

        # Transaction 3: User 1
        item = ArbiterSeqItem("item_user1")
        item.req = 2
        item.data0 = 0xAA
        item.data1 = 0x55

        await self.start_item(item)
        await self.finish_item(item)

        # Transaction 4: Both users
        item = ArbiterSeqItem("item_both")
        item.req = 3
        item.data0 = 0xA5
        item.data1 = 0x5A

        await self.start_item(item)
        await self.finish_item(item)
