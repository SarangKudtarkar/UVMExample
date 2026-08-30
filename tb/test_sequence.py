from tb.arbiter_sequence import ArbiterBasicSequence


def test_create_sequence():

    sequence = ArbiterBasicSequence()

    assert sequence is not None

    print("Sequence created successfully")
    print(sequence.get_name())
