import sys
import offgrid_ai

from operator import itemgetter
from offgrid_ai_pb2 import DataFile, NaturalGasType

def verify_lcoe_values(input_file):
    """This computes the LCOE for El Paso, TX with 125MW gas generators and all
    available solar & battery configurations. These are the same scenarios
    for which computed LCOE values are included in the spreadsheet so can be
    used to check the correctness of the code.
    """
    data_file = DataFile()
    with open(input_file, "rb") as f:
        data_file.ParseFromString(f.read())

    print("Solar;BESS;Generator;LCOE")
    for system_data in data_file.system_data:
        if (
            system_data.spec.location == "El Paso, TX"
            and round(system_data.spec.natural_gas_capacity_mw) == 125
        ):
            lcoe = offgrid_ai.breakeven_lcoe(
                system_data, offgrid_ai.build_standard_financial_inputs()
            )
            solar_size = round(system_data.spec.solar_capacity_mw)
            bess_size = round(system_data.spec.bess_max_power_mw)
            gas_size = round(system_data.spec.natural_gas_capacity_mw)
            print(f"{solar_size};{bess_size};{gas_size};{lcoe}")


def get_pareto_frontier(input_file, location, natural_gas_capacity_mw):
    """Compute the Pareto frontier that trades off between the LCOE & lifetime
       renewable percentage for a given location and natural gas generator
       capacity.
    """
    data_file = DataFile()
    with open(input_file, "rb") as f:
        data_file.ParseFromString(f.read())

    system_data_with_lcoe = []
    pareto_frontier = []

    for system_data in data_file.system_data:
        if (
            system_data.spec.location == location
            and round(system_data.spec.natural_gas_capacity_mw)
            == natural_gas_capacity_mw
        ):
            lcoe = offgrid_ai.breakeven_lcoe(
                system_data, offgrid_ai.build_standard_financial_inputs()
            )
            system_data_with_lcoe.append((system_data, lcoe))

    system_data_with_lcoe.sort(key=itemgetter(1))
    for system_data, lcoe in system_data_with_lcoe:
        if len(pareto_frontier) == 0:
            pareto_frontier.append((system_data, lcoe))
        else:
            previous_lifetime_renewable = offgrid_ai.lifetime_renewable_percentage(
                pareto_frontier[-1][0]
            )
            lifetime_renewable = offgrid_ai.lifetime_renewable_percentage(system_data)
            if lifetime_renewable > previous_lifetime_renewable:
                pareto_frontier.append((system_data, lcoe))

    for system_data, lcoe in pareto_frontier:
        lifetime_renewable = offgrid_ai.lifetime_renewable_percentage(system_data)
        solar_size = round(system_data.spec.solar_capacity_mw)
        bess_size = round(system_data.spec.bess_max_power_mw)
        print(
            f"LCOE:{lcoe} Lifetime renewable:{lifetime_renewable} - Solar:{solar_size}MW & BESS:{bess_size}MW"
        )


def generator_and_turbine_lcoe(input_file):
    """Compute and print the LCOE for 125MW gas generator & turbine systems with
       no solar or batteries.
    """
    data_file = DataFile()
    with open(input_file, "rb") as f:
        data_file.ParseFromString(f.read())

    for system_data in data_file.system_data:
        if (
            system_data.spec.location == "El Paso, TX"
            and round(system_data.spec.solar_capacity_mw) == 0
            and round(system_data.spec.bess_max_power_mw) == 0
            and round(system_data.spec.natural_gas_capacity_mw) == 125
        ):
            generator_lcoe = offgrid_ai.breakeven_lcoe(
                system_data, offgrid_ai.build_standard_financial_inputs()
            )
            system_data.spec.nat_gas_type = NaturalGasType.GAS_TURBINE
            turbine_lcoe = offgrid_ai.breakeven_lcoe(
                system_data, offgrid_ai.build_standard_financial_inputs()
            )
            print(f"Generator LCOE:{generator_lcoe} Turbine LCOE:{turbine_lcoe}")


def main():
    """Demonstration of code to calculate the LCOE & Pareto frontier."""
    if len(sys.argv) != 2:
        print("Usage: python test_offgrid_ai.py offgrid_ai_data.binarypb")
        sys.exit(1)

    input_file = sys.argv[1]

    print("LCOE value table:")
    verify_lcoe_values(input_file)
    print("El Paso, TX Pareto frontier")
    get_pareto_frontier(input_file, "El Paso, TX", 125)
    print("Amarillo, TX Pareto frontier")
    get_pareto_frontier(input_file, "Amarillo, TX", 125)

    print("Generator & Turbine LCOEs:")
    generator_and_turbine_lcoe(input_file)

if __name__ == "__main__":
    main()
