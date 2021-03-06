import os
import sys
import unittest
from ast import parse
from collections import namedtuple

from base_test_case import BaseTestCase
sys.path.insert(0, os.path.abspath('../pyt'))
from cfg import CFG, generate_ast, Node
from reaching_definitions import ReachingDefinitionsAnalysis
from fixed_point import FixedPointAnalysis

class FixedPointTest(BaseTestCase):
    connection = namedtuple('connection', 'constraintset element')
    def setUp(self):
        self.cfg_create_from_file('../example/example_inputs/example.py')

        self.analysis = FixedPointAnalysis(self.cfg, ReachingDefinitionsAnalysis)

    def assertInCfg(self, connections):
        ''' Assert that all connections in the connections list exists in the cfg,
        as well as all connections not in the list do not exist

        connections is a list of tuples where the node at index 0 of the tuple has to be in the new_constraintset of the node a index 1 of the tuple'''
        for connection in connections:
            self.assertIn(self.cfg.nodes[connection[0]], self.cfg.nodes[connection[1]].new_constraint, str(connection) + " expected to be connected")

        nodes = len(self.cfg.nodes)
        
        for element in range(nodes):
            for sets in range(nodes):
                if (element, sets) not in connections:
                    self.assertNotIn(self.cfg.nodes[element], self.cfg.nodes[sets].new_constraint, "(%s,%s)" % (element, sets)  +  " expected to be disconnected")

            
    def produce_iteration(self, iterationnumber):
        for x in range(iterationnumber):
            self.analysis.swap_constraints()
            self.analysis.fixpoint_iteration()
                    
    def test_fixpoint_algorithm_first_iteration(self):
        self.produce_iteration(1)

        self.assertInCfg([(1,1),(2,2),(4,4),(6,6),(7,7),(9,9),(10,10)])
        
        
    def test_fixpoint_algorithm_second_iteration(self):
        self.produce_iteration(2)

        self.assertInCfg([(1,1),
                          (2,2),
                          (2,3),(10,3),
                          (4,4),
                          (4,5),
                          (6,6),
                          (6,7),(7,7),
                          (7,8),
                          (9,9),
                          (9,10),(10,10)])
        

    def test_fixpoint_algorithm_third_iteration(self):
        self.produce_iteration(3)
        
        self.assertInCfg([(1,1),
                          (2,2),
                          (2,3),(9,3),(10,3),
                          (2,4),(4,4),(10,4),
                          (4,5),
                          (4,6),(6,6),
                          (4,7),(6,7),(7,7),
                          (6,8),(7,8),
                          (7,9),(9,9),
                          (9,10),(10,10),
                          (2,11),(10,11)])

    def test_fixpoint_algorithm_fourth_iteration(self):
        self.produce_iteration(4)

        self.assertInCfg([(1,1),
                          (2,2),
                          (2,3),(9,3),(10,3),
                          (2,4),(4,4),(9,4),(10,4),
                          (2,5),(4,5),(10,5),
                          (4,6),(6,6),
                          (4,7),(6,7),(7,7),
                          (4,8),(6,8),(7,8),
                          (7,9),(9,9),
                          (6,10),(9,10),(10,10),
                          (2,11),(9,11),(10,11),
                          (2,12),(10,12)])
        
    def test_fixpoint_algorithm_fifth_iteration(self):
        self.produce_iteration(5)

        self.assertInCfg([(1,1),
                          (2,2),
                          (2,3),(6,3),(9,3),(10,3),
                          (2,4),(4,4),(9,4),(10,4),
                          (2,5),(4,5),(9,5),(10,5),
                          (4,6),(6,6),(10,6),
                          (2,7),(4,7),(6,7),(7,7),
                          (4,8),(6,8),(7,8),
                          (4,9),(7,9),(9,9),
                          (4,10),(6,10),(9,10),(10,10),
                          (2,11),(9,11),(10,11),
                          (2,12),(9,12),(10,12)])

    def test_fixpoint_algorithm_sixth_iteration(self):
        self.produce_iteration(6)

        self.assertInCfg([(1,1),
                          (2,2),
                          (2,3),(4,3),(6,3),(9,3),(10,3),
                          (2,4),(4,4),(6,4),(9,4),(10,4),
                          (2,5),(4,5),(9,5),(10,5),
                          (4,6),(6,6),(10,6),
                          (2,7),(4,7),(6,7),(7,7),(9,7),
                          (2,8),(4,8),(6,8),(7,8),
                          (4,9),(7,9),(9,9),
                          (4,10),(6,10),(9,10),(10,10),
                          (2,11),(6,11),(9,11),(10,11),
                          (2,12),(9,12),(10,12)])

    def test_fixpoint_algorithm_seventh_iteration(self):
        self.produce_iteration(7)

        self.assertInCfg([(1,1),
                          (2,2),
                          (2,3),(4,3),(6,3),(9,3),(10,3),
                          (2,4),(4,4),(6,4),(9,4),(10,4),
                          (2,5),(4,5),(6,5),(9,5),(10,5),
                          (4,6),(6,6),(10,6),
                          (2,7),(4,7),(6,7),(7,7),(9,7),
                          (2,8),(4,8),(6,8),(7,8),(9,8),
                          (4,9),(7,9),(9,9),
                          (2,10),(4,10),(6,10),(9,10),(10,10),
                          (2,11),(4,11),(6,11),(9,11),(10,11),
                          (2,12),(6,12),(9,12),(10,12)])        

    def test_fixpoint_algorithm_eighth_iteration(self):
        self.produce_iteration(8)

        self.assertInCfg([(1,1),
                          (2,2),
                          (2,3),(4,3),(6,3),(9,3),(10,3),
                          (2,4),(4,4),(6,4),(9,4),(10,4),
                          (2,5),(4,5),(6,5),(9,5),(10,5),
                          (4,6),(6,6),(10,6),
                          (2,7),(4,7),(6,7),(7,7),(9,7),
                          (2,8),(4,8),(6,8),(7,8),(9,8),
                          (4,9),(7,9),(9,9),
                          (2,10),(4,10),(6,10),(9,10),(10,10),
                          (2,11),(4,11),(6,11),(9,11),(10,11),
                          (2,12),(4,12),(6,12),(9,12),(10,12)])        

        
    def test_fixpoint_algorithm_ninth_iteration(self):
        self.produce_iteration(9)

        self.assertInCfg([(1,1),
                          (2,2),
                          (2,3),(4,3),(6,3),(9,3),(10,3),
                          (2,4),(4,4),(6,4),(9,4),(10,4),
                          (2,5),(4,5),(6,5),(9,5),(10,5),
                          (4,6),(6,6),(10,6),
                          (2,7),(4,7),(6,7),(7,7),(9,7),
                          (2,8),(4,8),(6,8),(7,8),(9,8),
                          (4,9),(7,9),(9,9),
                          (2,10),(4,10),(6,10),(9,10),(10,10),
                          (2,11),(4,11),(6,11),(9,11),(10,11),
                          (2,12),(4,12),(6,12),(9,12),(10,12)])        

    def test_fixpoint_runner(self):
        self.analysis.fixpoint_runner()

        self.assertInCfg([(1,1),
                          (2,2),
                          (2,3),(4,3),(6,3),(9,3),(10,3),
                          (2,4),(4,4),(6,4),(9,4),(10,4),
                          (2,5),(4,5),(6,5),(9,5),(10,5),
                          (4,6),(6,6),(10,6),
                          (2,7),(4,7),(6,7),(7,7),(9,7),
                          (2,8),(4,8),(6,8),(7,8),(9,8),
                          (4,9),(7,9),(9,9),
                          (2,10),(4,10),(6,10),(9,10),(10,10),
                          (2,11),(4,11),(6,11),(9,11),(10,11),
                          (2,12),(4,12),(6,12),(9,12),(10,12)])
        
    def test_constraints_changed_true(self):
        self.produce_iteration(1)
        changed = self.analysis.constraints_changed()

        self.assertEqual(changed, True)

    def test_constraints_changed_false(self):
        self.produce_iteration(9)
        changed = self.analysis.constraints_changed()

        self.assertEqual(changed, False)
