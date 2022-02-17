invalid_property_value_test_cases = [
    #(<base_width>, <side_slope_1>, <side_slope_2>, <flow_depth>)  
    (0, 0, 0, -0.000001),
    (0, 0, -0.000001, 0),
    (0, -0.000001, 0, 0),
    (-0.000001, 0, 0, 0),
    (1, 1, 1, -1),
    (1, 1, -1, 1),
    (1, -1, 1, 1),
    (-1, 1, 1, 1)
]

undefined_flow_depth_test_cases = [
    #(<base_width>, <side_slope_1>, <side_slope_2>) 
    (4, 1, 1),
    (0, 0, 0),
    (99999, 99999, 99999),
]

input_output_test_cases = [
    #(
    #(<base_width>, <side_slope_1>, <side_slope_2>, <flow_depth>),
    #(<area>, <perimeter>, <hydraulic_radius>, (<centroid_x>, <centroid_y>), <flow_depth>)
    # ) 
    (
        (0, 0, 0, 0),
        (0, 0, 0, (0, 0), 0)
    ),
    (
        (4, 1, 2, 2), 
        (14, 11.300563, 1.238876, (4.571428, 0.857143), 2)
    ),
    (
        (4, 0, 0, 3), 
        (12, 10, 1.2, (2, 1.5), 3)
    ),
    (
        (0, 1, 1, 5), 
        (25, 14.142135, 1.767767, (5, 1.666667), 5)
    )
]

runtime_exceptions_test_cases = []