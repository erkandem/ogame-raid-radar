from src import utils


class TestOrePrice:
    price = {
        'metal': 100,
        'crystal': 100,
        'deuterium': 100,
    }

    def test_lazy_instantiation(self):
        op1 = utils.OrePrice(**self.price)
        op2 = utils.OrePrice()
        op2.__dict__.update(**self.price)
        assert op1.metal == op2.metal
        assert op1.crystal == op2.crystal
        assert op1.deuterium == op2.deuterium

    def test_equality(self):
        op1 = utils.OrePrice(**self.price)
        op2 = utils.OrePrice(**self.price)
        assert op1 == op2

    def test_subtraction(self):
        op1 = utils.OrePrice(**self.price)
        op2 = utils.OrePrice(**self.price)
        op3 = op1 - op2
        assert op3.metal == 0
        assert op3.crystal == 0
        assert op3.deuterium == 0

    def test_addition(self):
        op1 = utils.OrePrice(**self.price)
        op2 = utils.OrePrice(**self.price)
        op3 = op1 + op2
        assert op3.metal == 2 * self.price['metal']
        assert op3.crystal == 2 * self.price['crystal']
        assert op3.deuterium == 2 * self.price['deuterium']

    def test_to_dict(self):
        op = utils.OrePrice(**self.price)
        assert op.to_dict() == self.price

    def test_multiplication(self):
        op = utils.OrePrice(**self.price)
        factor = 10
        op = op * factor
        assert op.metal == factor * self.price['metal']
        assert op.crystal == factor * self.price['crystal']
        assert op.deuterium == factor * self.price['deuterium']

    def test_exponentiation(self):
        op = utils.OrePrice(**self.price)
        exponent = 2
        op = op ** exponent
        assert op.metal == self.price['metal'] ** exponent
        assert op.crystal == self.price['crystal'] ** exponent
        assert op.deuterium == self.price['deuterium'] ** exponent

    def test_get_metal_equivalent_units(self):
        pass

