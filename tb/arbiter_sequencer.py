from pyuvm import uvm_sequencer


class ArbiterSequencer(uvm_sequencer):

    def __init__(self, name="ArbiterSequencer", parent=None):
        super().__init__(name, parent)

    async def run_phase(self):
        print(">>> SEQUENCER run_phase START")

        while True:
            print(">>> SEQUENCER waiting for item")
            next_item = await self.seq_q.get()

            print(f">>> SEQUENCER got item: {next_item}")

            await self.seq_item_export.put_req(next_item)

            print(">>> SEQUENCER sent item to driver")
