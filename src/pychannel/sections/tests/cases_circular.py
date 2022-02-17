invalid_property_value_test_cases = [   
    (0, -0.000001),
    (-0.000001, 0)
]

undefined_flow_depth_test_cases = [
    (0,),
    (1,),
    (10000000000000,)
]

unavailable_height_test_cases = [
    (1, 3),
    (0, 0.0000001),
    (1, 2.0000001)
]

input_output_test_cases = [
    ((0, 0),(0, 0, 0, (0, 0), 0)),
    ((4, 1), (14, 11.300563, 1.238876, (4.571428, 0.857143), 2)),
    ((4, 0), (12, 10, 1.2, (2, 1.5), 3)),
    ((0, 1), (25, 14.142135, 1.767767, (5, 1.666667), 5))
]

runtime_exceptions_test_cases = []