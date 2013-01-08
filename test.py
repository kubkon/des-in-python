#!/usr/bin/env python
# encoding: utf-8

import unittest
import simulator.tests.mm1 as mm1
import simulator.tests.sim as sim


# Run tests
# 1. MM1EventHandler class
unittest.TextTestRunner(verbosity=2).run( \
    unittest.TestLoader().loadTestsFromTestCase(mm1.MM1EventHandlerTests))
# 2. SimulatorEngine class
unittest.TextTestRunner(verbosity=2).run( \
    unittest.TestLoader().loadTestsFromTestCase(sim.SimulationEngineTests))
# 3. Event class
unittest.TextTestRunner(verbosity=2).run( \
    unittest.TestLoader().loadTestsFromTestCase(sim.EventTests))

