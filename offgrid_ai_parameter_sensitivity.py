import sys
import offgrid_ai

from operator import itemgetter
from offgrid_ai_pb2 import DataFile, FinancialInputs, SystemData, NaturalGasType


def get_system(
    data_file: DataFile,
    location,
    solar_capacity_mw,
    bess_max_power_mw,
    natural_gas_capacity_mw,
) -> SystemData:
    systems = []
    for system_data in data_file.system_data:
        if (
            system_data.spec.location == location
            and round(system_data.spec.solar_capacity_mw) == solar_capacity_mw
            and round(system_data.spec.bess_max_power_mw) == bess_max_power_mw
            and round(system_data.spec.natural_gas_capacity_mw)
            == natural_gas_capacity_mw
        ):
            systems.append(system_data)
    if len(systems) != 1:
        raise ValueError("Multiple matching systems")
    return systems[0]

def compute_lcoes(
    data_file: DataFile,
    financial_inputs: FinancialInputs,
    location,
    natural_gas_capacity_mw,
    both_gas,
):
    system_data_with_lcoe = []

    for system_data in data_file.system_data:
        if (
            system_data.spec.location == location
            and round(system_data.spec.natural_gas_capacity_mw)
            == natural_gas_capacity_mw
        ):
            lcoe = offgrid_ai.breakeven_lcoe(system_data, financial_inputs)
            system_data_with_lcoe.append((system_data, lcoe))
            if both_gas:
                turbine_system_data = SystemData()
                turbine_system_data.CopyFrom(system_data)
                turbine_system_data.spec.nat_gas_type = NaturalGasType.GAS_TURBINE
                lcoe = offgrid_ai.breakeven_lcoe(turbine_system_data, financial_inputs)
                system_data_with_lcoe.append((turbine_system_data, lcoe))
    return system_data_with_lcoe


def get_lowest_lcoe_system(
    data_file: DataFile,
    financial_inputs: FinancialInputs,
    location,
    natural_gas_capacity_mw,
    both_gas,
) -> SystemData:
    """Compute the lowest LCOE sytems for a given set of financial inputs, location and
    natural gas generator size.
    """
    system_data_with_lcoe = []

    for system_data in data_file.system_data:
        if (
            system_data.spec.location == location
            and round(system_data.spec.natural_gas_capacity_mw)
            == natural_gas_capacity_mw
        ):
            lcoe = offgrid_ai.breakeven_lcoe(system_data, financial_inputs)
            system_data_with_lcoe.append((system_data, lcoe))
            if both_gas:
                turbine_system_data = SystemData()
                turbine_system_data.CopyFrom(system_data)
                turbine_system_data.spec.nat_gas_type = NaturalGasType.GAS_TURBINE
                lcoe = offgrid_ai.breakeven_lcoe(turbine_system_data, financial_inputs)
                system_data_with_lcoe.append((turbine_system_data, lcoe))

    system_data_with_lcoe.sort(key=itemgetter(1))
    lowest_lcoe_system = system_data_with_lcoe[0][0]
    return lowest_lcoe_system


def print_lcoe(
    system_data: SystemData, financial_inputs: FinancialInputs, components: bool
):
    lcoe = offgrid_ai.breakeven_lcoe(system_data, financial_inputs)
    digits_rounded = 4
    lcoe_rounded = round(lcoe, digits_rounded)
    offgrid_ai.print_system_spec(system_data)
    lifetime_renewable = round(
        100 * offgrid_ai.lifetime_renewable_percentage(system_data), digits_rounded
    )
    print(f"Lifetime renewable percentage: {lifetime_renewable}%")
    print(f"LCOE: ${lcoe_rounded}")
    if components:
        total_costs_npv = -(
            offgrid_ai.equity_capex_npv(system_data, financial_inputs)
            + offgrid_ai.debt_service_npv(system_data, financial_inputs)
            + offgrid_ai.tax_benefit_npv(system_data, financial_inputs, lcoe)
            + offgrid_ai.variable_om_npv(system_data, financial_inputs)
            + offgrid_ai.fixed_om_npv(system_data, financial_inputs)
            + offgrid_ai.fuel_cost_npv(system_data, financial_inputs)
        )
        equity_capex_per_mwh = round(
            -offgrid_ai.equity_capex_npv(system_data, financial_inputs)
            / total_costs_npv
            * lcoe,
            digits_rounded,
        )
        debt_service_per_mwh = round(
            -offgrid_ai.debt_service_npv(system_data, financial_inputs)
            / total_costs_npv
            * lcoe,
            digits_rounded,
        )
        tax_benefit_per_mwh = round(
            -offgrid_ai.tax_benefit_npv(system_data, financial_inputs, lcoe)
            / total_costs_npv
            * lcoe,
            digits_rounded,
        )
        variable_om_per_mwh = round(
            -offgrid_ai.variable_om_npv(system_data, financial_inputs)
            / total_costs_npv
            * lcoe,
            digits_rounded,
        )
        fixed_om_per_mwh = round(
            -offgrid_ai.fixed_om_npv(system_data, financial_inputs)
            / total_costs_npv
            * lcoe,
            digits_rounded,
        )
        fuel_cost_per_mwh = round(
            -offgrid_ai.fuel_cost_npv(system_data, financial_inputs)
            / total_costs_npv
            * lcoe,
            digits_rounded,
        )
        print("LCOE Components:")
        print(f"Equity capex/MWh: ${equity_capex_per_mwh}")
        print(f"Debt service/MWh: ${debt_service_per_mwh}")
        print(f" Tax benefit/MWh: ${tax_benefit_per_mwh}")
        print(f"   Fixed O&M/MWh: ${fixed_om_per_mwh}")
        print(f"Variable O&M/MWh: ${variable_om_per_mwh}")
        print(f"   Fuel cost/MWh: ${fuel_cost_per_mwh}")

def main():
    """Demonstration of code to calculate the LCOE & Pareto frontier."""
    if len(sys.argv) != 2:
        print("Usage: python offgrid_ai_parameter_sensitivity.py offgrid_ai_data.binarypb")
        sys.exit(1)

    file_name = sys.argv[1]
    data_file = DataFile()
    with open(file_name, "rb") as f:
        data_file.ParseFromString(f.read())

    # Basic example of using this to find the lowest cost system and calculate the LCOE for a specific system.
    lowest_lcoe_system = get_lowest_lcoe_system(
        data_file, offgrid_ai.build_standard_financial_inputs(), "El Paso, TX", 125, False
    )
    all_generators_system = get_system(data_file, "El Paso, TX", 0, 0, 125)
    all_turbines_system = SystemData()
    all_turbines_system.CopyFrom(all_generators_system)
    all_turbines_system.spec.nat_gas_type = NaturalGasType.GAS_TURBINE

    print("El Paso, TX Lowest LCOE system:")
    print_lcoe(lowest_lcoe_system, offgrid_ai.build_standard_financial_inputs(), True)
    print("All Generators System LCOE:")
    print_lcoe(all_generators_system, offgrid_ai.build_standard_financial_inputs(), True)
    print("All Generators System LCOE:")
    print_lcoe(all_turbines_system, offgrid_ai.build_standard_financial_inputs(), True)

    # Example of computing results for many different potential system locations.
    print("Lowest cost by location")
    lowest_lcoe_amarillo = get_lowest_lcoe_system(
        data_file, offgrid_ai.build_standard_financial_inputs(), "Amarillo, TX", 125, False
    )
    print_lcoe(lowest_lcoe_amarillo, offgrid_ai.build_standard_financial_inputs(), True)
    lowest_lcoe_beryl = get_lowest_lcoe_system(
        data_file, offgrid_ai.build_standard_financial_inputs(), "Beryl Junction, UT", 125, False
    )
    print_lcoe(lowest_lcoe_beryl, offgrid_ai.build_standard_financial_inputs(), True)
    lowest_lcoe_el_paso = get_lowest_lcoe_system(
        data_file, offgrid_ai.build_standard_financial_inputs(), "El Paso, TX", 125, False
    )
    print_lcoe(lowest_lcoe_el_paso, offgrid_ai.build_standard_financial_inputs(), True)
    lowest_lcoe_lovelock = get_lowest_lcoe_system(
        data_file, offgrid_ai.build_standard_financial_inputs(), "Lovelock, NV", 125, False
    )
    print_lcoe(lowest_lcoe_lovelock, offgrid_ai.build_standard_financial_inputs(), True)
    lowest_lcoe_komelik = get_lowest_lcoe_system(
        data_file, offgrid_ai.build_standard_financial_inputs(), "North Komelik, AZ", 125, False
    )
    print_lcoe(lowest_lcoe_komelik, offgrid_ai.build_standard_financial_inputs(), True)
    lowest_lcoe_trinidad = get_lowest_lcoe_system(
        data_file, offgrid_ai.build_standard_financial_inputs(), "Trinidad, CO", 125, False
    )
    print_lcoe(lowest_lcoe_trinidad, offgrid_ai.build_standard_financial_inputs(), True)
    lowest_lcoe_willcox = get_lowest_lcoe_system(
        data_file, offgrid_ai.build_standard_financial_inputs(), "Willcox, NM", 125, False
    )
    print_lcoe(lowest_lcoe_willcox, offgrid_ai.build_standard_financial_inputs(), True)
    lowest_lcoe_yuma = get_lowest_lcoe_system(
        data_file, offgrid_ai.build_standard_financial_inputs(), "Yuma, AZ", 125, False
    )
    print_lcoe(lowest_lcoe_yuma, offgrid_ai.build_standard_financial_inputs(), True)

    # Examples of using this to print a Pareto frontier.
    normal_itc_pareto_frontier = offgrid_ai.find_pareto_frontier(compute_lcoes(data_file, offgrid_ai.build_standard_financial_inputs(), "El Paso, TX", 125, False))
    print("Normal ITC Pareto frontier:")
    for system_data, _ in normal_itc_pareto_frontier:
        lcoe = offgrid_ai.breakeven_lcoe(system_data, offgrid_ai.build_standard_financial_inputs())
        lifetime_renewable = offgrid_ai.lifetime_renewable_percentage(system_data)
        print(f"{lifetime_renewable},{lcoe},{system_data.spec.solar_capacity_mw},{system_data.spec.bess_max_power_mw}")

    energy_community_financial_inputs = offgrid_ai.build_standard_financial_inputs()
    energy_community_financial_inputs.investment_tax_credit = 0.4
    energy_community_itc_pareto_frontier = offgrid_ai.find_pareto_frontier(compute_lcoes(data_file, energy_community_financial_inputs, "El Paso, TX", 125, False))
    print("Energy Community ITC Pareto frontier:")
    for system_data, _ in energy_community_itc_pareto_frontier:
        lcoe = offgrid_ai.breakeven_lcoe(system_data, energy_community_financial_inputs)
        lifetime_renewable = offgrid_ai.lifetime_renewable_percentage(system_data)
        print(f"{lifetime_renewable},{lcoe},{system_data.spec.solar_capacity_mw},{system_data.spec.bess_max_power_mw}")

    # The below calculates the optimal system for a 2D grid of prices under different tax credit scenarios.
    print("Lowest cost system for solar & battery price drop with normal ITC")
    for module_price_cents in range(22, 1, -1):
        for bess_price in range(200, 90, -10):
            financial_inputs = offgrid_ai.build_standard_financial_inputs()
            financial_inputs.capex_inputs.bess_capex.bess_units = bess_price
            financial_inputs.capex_inputs.solar_capex.modules = module_price_cents / 100.
            lowest_lcoe_system = get_lowest_lcoe_system(
                data_file, financial_inputs, "El Paso, TX", 125, False
            )
            lcoe = offgrid_ai.breakeven_lcoe(lowest_lcoe_system, financial_inputs)
            lifetime_renewable = offgrid_ai.lifetime_renewable_percentage(lowest_lcoe_system)
            print(f"{module_price_cents},{bess_price},{lifetime_renewable},{lcoe},{lowest_lcoe_system.spec.solar_capacity_mw},{lowest_lcoe_system.spec.bess_max_power_mw}")

    print("Lowest cost system for solar & battery price drop with energy community 40% ITC")
    for module_price_cents in range(22, 1, -1):
        for bess_price in range(200, 90, -10):
            financial_inputs = offgrid_ai.build_standard_financial_inputs()
            financial_inputs.investment_tax_credit = 0.4
            financial_inputs.capex_inputs.bess_capex.bess_units = bess_price
            financial_inputs.capex_inputs.solar_capex.modules = module_price_cents / 100.
            lowest_lcoe_system = get_lowest_lcoe_system(
                data_file, financial_inputs, "El Paso, TX", 125, False
            )
            lcoe = offgrid_ai.breakeven_lcoe(lowest_lcoe_system, financial_inputs)
            lifetime_renewable = offgrid_ai.lifetime_renewable_percentage(lowest_lcoe_system)
            print(f"{module_price_cents},{bess_price},{lifetime_renewable},{lcoe},{lowest_lcoe_system.spec.solar_capacity_mw},{lowest_lcoe_system.spec.bess_max_power_mw}")


if __name__ == "__main__":
    main()
