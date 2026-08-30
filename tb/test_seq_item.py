from tb.arbiter_seq_item import ArbiterSeqItem


def test_create_transaction():

    item = ArbiterSeqItem()

    item.req = 3
    item.data0 = 0xA5
    item.data1 = 0x5A

    print(item)

    assert item.req == 3
    assert item.data0 == 0xA5
    assert item.data1 == 0x5A
