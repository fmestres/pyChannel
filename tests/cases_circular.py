invalid_property_value_test_cases = [  
    #(<radius>, <flow_depth>) 
    (0, -0.000001),
    (-0.000001, 0)
]

undefined_flow_depth_test_cases = [
    #(<radius>, <flow_depth>) 
    (0,),
    (1,),
    (10000000000000,)
]

unavailable_height_test_cases = [
    #(<radius>, <flow_depth>) 
    (1, 3),
    (0, 0.0000001),
    (1, 2.0000001)
]

input_output_test_cases = [
    #(
    #(<radius>, <flow_depth>,
    #(<area>, <perimeter>, <hydraulic_radius>, (<centroid_x>, <centroid_y>), <flow_depth>)
    # ) 
    ((0, 0), (0, 0, 0, (0, 0), 0)),
    ((4.1, 2.9),(16.707437, 10.444872, 1.599582, (4.1, 1.204416), 2.9)),
    ((9.4, 9.6), (142.555280, 29.931001, 4.762797, (9.4, 4.081629), 9.6)),
    ((1.5, 2.5), (6.294213, 6.901572, 0.911997, (1.5, 1.148024), 2.5)),
    ((1, 2), (3.141593, 6.283185, 0.5, (1, 1), 2))
]

