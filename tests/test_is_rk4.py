from unittest.mock import patch

# Assuming your classes are defined as follows (or imported from your module)
from py_ballisticcalc import DragModel, TableG1, Ammo, Weapon, Distance, Shot, Atmo, ZeroFindingError, RangeError
from py_ballisticcalc.generics.engine import EngineProtocol
from py_ballisticcalc.interface import Calculator

from RKballistic import RK4TrajectoryCalc


class TestIsRK4:
    def test_entry_point_loaded(self, ):
        dm = DragModel(0.365, TableG1, 69, 0.223, 0.9)
        ammo = Ammo(dm, 2600)
        weapon = Weapon(Distance(3.2, Distance.Inch))
        atmosphere = Atmo.icao()
        calc = Calculator(_engine="RKballistic")
        zero_angle = calc.barrel_elevation_for_target(Shot(weapon=weapon, ammo=ammo, atmo=atmosphere),
                                                      Distance(100, Distance.Yard))

        calc = Calculator(_engine="RKballistic")
        assert isinstance(calc._calc.__class__,
                          EngineProtocol), "Not implements EngineProtocol: %s" % calc._engine.__class__
        assert isinstance(calc._calc, RK4TrajectoryCalc), "Not is RK4TrajectoryCalc"

    def test_uses_rk4_integrate(self):
        dm = DragModel(0.365, TableG1, 69, 0.223, 0.9)
        ammo = Ammo(dm, 2600)
        weapon = Weapon(Distance(3.2, Distance.Inch))
        atmosphere = Atmo.icao()

        # Step 1: Create the Calculator instance FIRST.
        # This will cause it to load RK4TrajectoryCalc via the entry point.
        calc = Calculator(_engine="RKballistic")

        # Step 2: Now that calc._calc holds an instance of RK4TrajectoryCalc,
        # patch the 'integrate' method directly on that specific instance.
        with patch.object(calc._calc, '_integrate') as mock_integrate:
            try:
                # Step 3: Call the method that should trigger 'integrate'.
                calc.barrel_elevation_for_target(Shot(weapon=weapon, ammo=ammo, atmo=atmosphere),
                                                 Distance(100, Distance.Yard))
            except (ZeroFindingError, RangeError):
                pass  # skip calculation errors, to test only compatibility matching

            # Step 4: Assert that the mock_integrate method was called.
            # This should now pass because you patched the actual object being used.
            mock_integrate.assert_called()
