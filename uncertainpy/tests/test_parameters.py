import unittest
import os

import chaospy as cp


from uncertainpy import Parameter, Parameters


class TestParameter(unittest.TestCase):
    def setUp(self):
        self.parameter = Parameter("gbar_Na", 120)

        self.parameter_filename = "example_hoc.hoc"

    def test_initNone(self):
        parameter = Parameter("gbar_Na", 120)

        self.assertEqual(parameter.name, "gbar_Na")
        self.assertEqual(parameter.value, 120)


    def test_initFunction(self):
        def distribution(x):
            return cp.Uniform(x - 10, x + 10)

        parameter = Parameter("gbar_Na", 120, distribution)

        self.assertEqual(parameter.name, "gbar_Na")
        self.assertEqual(parameter.value, 120)
        self.assertIsInstance(parameter.parameter_space, cp.Dist)


    def test_initChaospy(self):
        parameter = Parameter("gbar_Na", 120, cp.Uniform(110, 130))

        self.assertTrue(parameter.name, "gbar_Na")
        self.assertTrue(parameter.value, 120)
        self.assertIsInstance(parameter.parameter_space, cp.Dist)


    def test_setDistributionNone(self):
        distribution = None
        self.parameter.setDistribution(distribution)

        self.assertIsNone(self.parameter.parameter_space)


    def test_setDistributionFunction(self):
        def distribution_function(x):
            return cp.Uniform(x - 10, x + 10)

        self.parameter.setDistribution(distribution_function)

        # self.assertEqual(self.parameter.parameter_space, cp.Uniform(110, 130))
        self.assertIsInstance(self.parameter.parameter_space, cp.Dist)

        def test_setDistributionFunctionNotDistReturn(self):
            def distribution_function(x):
                return x

            with self.assertRaises(TypeError):
                self.parameter.setDistribution(distribution_function)


    def test_setDistributionInt(self):
        distribution = 1
        with self.assertRaises(TypeError):
            self.parameter.setDistribution(distribution)


    def test_setDistributionChaospy(self):
        distribution = cp.Uniform(110, 130)
        self.parameter.setDistribution(distribution)

        # self.assertEqual(self.parameter.parameter_space, cp.Uniform(110, 130))
        self.assertIsInstance(self.parameter.parameter_space, cp.Dist)


    def test_setParameterValues(self):
        self.folder = os.path.dirname(os.path.realpath(__file__))
        self.test_data_dir = os.path.join(self.folder, "data")


        self.parameter = Parameter("test", 120)

        self.parameter.setParameterValue(os.path.join(self.test_data_dir,
                                                      self.parameter_filename), 12)





class TestParameters(unittest.TestCase):
    # def setUp(self):
    #     parameterlist = [["gbar_Na", 120, None],
    #                      ["gbar_K", 36, None],
    #                      ["gbar_l", 0.3, None]]
    #
    #     self.parameters = Parameters(parameterlist)
    #

    def test_initListNone(self):
        parameterlist = [["gbar_Na", 120, None],
                         ["gbar_K", 36, None],
                         ["gbar_l", 0.3, None]]

        parameters = Parameters(parameterlist)


    def test_initListChaospy(self):
        parameterlist = [["gbar_Na", 120, cp.Uniform(110, 130)],
                         ["gbar_K", 36, cp.Normal(36, 1)],
                         ["gbar_l", 0.3, cp.Chi(1, 1, 0.3)]]

        parameters = Parameters(parameterlist)


    def test_initObject(self):
        parameterlist = [Parameter("gbar_Na", 120, cp.Uniform(110, 130)),
                         Parameter("gbar_K", 36),
                         Parameter("gbar_l", 10.3)]

        parameters = Parameters(parameterlist)


    def test_getitem(self):
        parameterlist = [["gbar_Na", 120, None],
                         ["gbar_K", 36, None],
                         ["gbar_l", 0.3, None]]

        self.parameters = Parameters(parameterlist)

        self.assertIsInstance(self.parameters["gbar_Na"], Parameter)


    def test_setDistribution(self):
        parameterlist = [["gbar_Na", 120, None],
                         ["gbar_K", 36, None],
                         ["gbar_l", 0.3, None]]

        self.parameters = Parameters(parameterlist)

        def distribution_function(x):
            return cp.Uniform(x - 10, x + 10)

        self.parameters.setDistribution("gbar_Na", distribution_function)

        self.assertIsInstance(self.parameters["gbar_Na"].parameter_space, cp.Dist)


    def setAllDistributions(self):
        parameterlist = [["gbar_Na", 120, None],
                         ["gbar_K", 36, None],
                         ["gbar_l", 0.3, None]]

        self.parameters = Parameters(parameterlist)


        def distribution_function(x):
            return cp.Uniform(x - 10, x + 10)

        self.parameters.setAllDistributions(distribution_function)

        self.assertIsInstance(self.parameters["gbar_Na"].parameter_space, cp.Dist)
        self.assertIsInstance(self.parameters["gbar_K"].parameter_space, cp.Dist)
        self.assertIsInstance(self.parameters["gbar_l"].parameter_space, cp.Dist)


    def test_getUncertainName(self):
        parameterlist = [["gbar_Na", 120, cp.Uniform(110, 130)],
                         ["gbar_K", 36, cp.Normal(36, 1)],
                         ["gbar_l", 0.3, None]]

        self.parameters = Parameters(parameterlist)
        result = self.parameters.getUncertain()

        self.assertIn("gbar_Na", result)
        self.assertIn("gbar_K", result)
        self.assertNotIn("gbar_l", result)


    def test_getUncertainValue(self):
        parameterlist = [["gbar_Na", 120, cp.Uniform(110, 130)],
                         ["gbar_K", 36, cp.Normal(36, 1)],
                         ["gbar_l", 0.3, None]]

        self.parameters = Parameters(parameterlist)
        result = self.parameters.getUncertain("value")


        self.assertIn(120, result)
        self.assertIn(36, result)
        self.assertNotIn(0.3, result)


    def test_getUncertainParameterSpace(self):
        parameterlist = [["gbar_Na", 120, cp.Uniform(110, 130)],
                         ["gbar_K", 36, cp.Normal(36, 1)],
                         ["gbar_l", 0.3, None]]

        self.parameters = Parameters(parameterlist)
        result = self.parameters.getUncertain("parameter_space")

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], cp.Dist)
        self.assertIsInstance(result[1], cp.Dist)


    def test_getName(self):
        parameterlist = [["gbar_Na", 120, cp.Uniform(110, 130)],
                         ["gbar_K", 36, cp.Normal(36, 1)],
                         ["gbar_l", 0.3, cp.Chi(1, 1, 0.3)]]

        self.parameters = Parameters(parameterlist)

        result = self.parameters.get()

        self.assertIn("gbar_Na", result)
        self.assertIn("gbar_K", result)
        self.assertIn("gbar_l", result)


    def test_getValue(self):
        parameterlist = [["gbar_Na", 120, cp.Uniform(110, 130)],
                         ["gbar_K", 36, cp.Normal(36, 1)],
                         ["gbar_l", 0.3, cp.Chi(1, 1, 0.3)]]
        self.parameters = Parameters(parameterlist)

        result = self.parameters.get("value")


        self.assertIn(120, result)
        self.assertIn(36, result)
        self.assertIn(0.3, result)


    def test_getParameterSpace(self):
        parameterlist = [["gbar_Na", 120, cp.Uniform(110, 130)],
                         ["gbar_K", 36, cp.Normal(36, 1)],
                         ["gbar_l", 0.3, cp.Chi(1, 1, 0.3)]]

        self.parameters = Parameters(parameterlist)
        result = self.parameters.get("parameter_space")

        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], cp.Dist)
        self.assertIsInstance(result[1], cp.Dist)
        self.assertIsInstance(result[2], cp.Dist)


if __name__ == "__main__":
    unittest.main()
