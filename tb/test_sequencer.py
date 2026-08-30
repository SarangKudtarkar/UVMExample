from tb.arbiter_sequencer import ArbiterSequencer


def test_create_sequencer():

    sequencer = ArbiterSequencer()

    assert sequencer is not None

    print("Sequencer created successfully")
    print(sequencer.get_name())
