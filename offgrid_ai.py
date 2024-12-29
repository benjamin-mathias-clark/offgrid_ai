from offgrid_ai_pb2 import SystemData, FinancialInputs, NaturalGasType


def after_tax_equity_npv(
    system_data: SystemData, financial_inputs: FinancialInputs, lcoe: float
) -> float:
    """Computer the after-tax equity NPV for the given system, costs and LCOE."""
    return (
        ebitda_npv(system_data, financial_inputs, lcoe)
        + debt_service_npv(system_data, financial_inputs)
        + tax_benefit_npv(system_data, financial_inputs, lcoe)
        + equity_capex_npv(system_data, financial_inputs)
    )


def ebitda_npv(
    system_data: SystemData, financial_inputs: FinancialInputs, lcoe: float
) -> float:
    """Computes the NPV of the EBITDA over the project lifetime."""
    operating_year_ebitdas = []
    for production in system_data.production:
        revenue = lcoe * production.load_served_mwh
        fuel_cost = (
            -production.generator_fuel_mmbtu
            * financial_inputs.fuel_price_mmbtu
            * (1 + financial_inputs.fuel_escalator) ** (production.year - 1)
        )
        if system_data.spec.nat_gas_type == NaturalGasType.GAS_TURBINE:
            fuel_cost *= financial_inputs.turbine_vs_generator_fuel_consumption_ratio
        solar_fixed_om = (
            -financial_inputs.opex_inputs.solar_fixed_om_kw
            * system_data.spec.solar_capacity_mw
            * 1000
            * (1 + financial_inputs.om_escalator) ** (production.year - 1)
        )
        battery_fixed_om = (
            -financial_inputs.opex_inputs.bess_fixed_om_kw
            * system_data.spec.bess_max_power_mw
            * 1000
            * (1 + financial_inputs.om_escalator) ** (production.year - 1)
        )
        generator_fixed_om = (
            -financial_inputs.opex_inputs.generators_fixed_om_kw
            * system_data.spec.natural_gas_capacity_mw
            * 1000
            * (1 + financial_inputs.om_escalator) ** (production.year - 1)
            if system_data.spec.nat_gas_type == NaturalGasType.GENERATOR
            else 0
        )
        generator_variable_om = (
            -financial_inputs.opex_inputs.generators_variable_om_kwh
            * production.generator_output_mwh
            * 1000
            * (1 + financial_inputs.om_escalator) ** (production.year - 1)
            if system_data.spec.nat_gas_type == NaturalGasType.GENERATOR
            else 0
        )
        gas_turbine_fixed_om = (
            -financial_inputs.opex_inputs.gas_turbines_fixed_om_kw
            * system_data.spec.natural_gas_capacity_mw
            * 1000
            * (1 + financial_inputs.om_escalator) ** (production.year - 1)
            if system_data.spec.nat_gas_type == NaturalGasType.GAS_TURBINE
            else 0
        )
        gas_turbines_variable_om = (
            -financial_inputs.opex_inputs.gas_turbines_variable_om_kwh
            * production.generator_output_mwh
            * 1000
            * (1 + financial_inputs.om_escalator) ** (production.year - 1)
            if system_data.spec.nat_gas_type == NaturalGasType.GAS_TURBINE
            else 0
        )
        bos_fixed_om = (
            -financial_inputs.opex_inputs.bos_fixed_om_kw
            * system_data.spec.load_mw
            * 1000
            * (1 + financial_inputs.om_escalator) ** (production.year - 1)
        )
        soft_costs_om = (
            -financial_inputs.opex_inputs.soft_costs
            * (hard_capex(system_data, financial_inputs) - gas_turbine_capex_spend(system_data, financial_inputs))
            * (1 + financial_inputs.om_escalator) ** (production.year - 1)
        )
        total_operating_costs = (
            fuel_cost
            + solar_fixed_om
            + battery_fixed_om
            + generator_fixed_om
            + generator_variable_om
            + gas_turbine_fixed_om
            + gas_turbines_variable_om
            + bos_fixed_om
            + soft_costs_om
        )
        ebitda = revenue + total_operating_costs
        operating_year_ebitdas.append((production.year, ebitda))
    return calc_npv(
        operating_year_ebitdas,
        financial_inputs.cost_of_equity,
        financial_inputs.construction_time,
    )


def total_capex(system_data: SystemData, financial_inputs: FinancialInputs) -> float:
    """Compute the total capital expenditures that the project requires."""
    hard_capex_spend = hard_capex(system_data, financial_inputs)
    soft_cost_capex = financial_inputs.capex_inputs.soft_cost_capex
    soft_cost_percentage = (
        soft_cost_capex.general_conditions
        + soft_cost_capex.epc_overhead
        + soft_cost_capex.design_engineering_and_surveys
        + soft_cost_capex.permitting_and_inspection
        + soft_cost_capex.startup_and_commissioning
        + soft_cost_capex.insurance
        + soft_cost_capex.taxes
    )
    return hard_capex_spend * (1 + soft_cost_percentage) - gas_turbine_capex_spend(system_data, financial_inputs) * soft_cost_percentage


def hard_capex(system_data: SystemData, financial_inputs: FinancialInputs) -> float:
    """Compute the hard capital expenditures."""
    solar_capex = financial_inputs.capex_inputs.solar_capex
    bess_capex = financial_inputs.capex_inputs.bess_capex
    generator_capex = financial_inputs.capex_inputs.generator_capex
    system_integration_capex = financial_inputs.capex_inputs.system_integration_capex

    solar_capex_spend = (
        (
            solar_capex.modules
            + solar_capex.inverters
            + solar_capex.racking_and_foundations
            + solar_capex.balance_of_system
            + solar_capex.labor
        )
        * 1000000
        * system_data.spec.solar_capacity_mw
    )
    bess_capex_spend = (
        (bess_capex.bess_units + bess_capex.balance_of_system + bess_capex.labor)
        * 1000
        * system_data.spec.bess_energy_capacity_mwh
    )
    generators_capex_spend = (
        (
            generator_capex.gensets
            + generator_capex.balance_of_system
            + generator_capex.labor
        )
        * 1000
        * system_data.spec.natural_gas_capacity_mw
        if system_data.spec.nat_gas_type == NaturalGasType.GENERATOR
        else 0
    )
    system_integration_capex_spend = (
        (
            system_integration_capex.microgrid_switchgear_transformers_etc
            + system_integration_capex.controls
            + system_integration_capex.labor
        )
        * 1000
        * system_data.spec.load_mw
    )
    return (
        solar_capex_spend
        + bess_capex_spend
        + generators_capex_spend
        + gas_turbine_capex_spend(system_data, financial_inputs)
        + system_integration_capex_spend
    )

def gas_turbine_capex_spend(system_data: SystemData, financial_inputs: FinancialInputs) -> float:
    """Compute the gas turbine capital expenditures."""
    gas_turbine_capex = financial_inputs.capex_inputs.gas_turbine_capex

    gas_turbine_capex_spend = (
        (
            gas_turbine_capex.gas_turbines
            + gas_turbine_capex.balance_of_system
            + gas_turbine_capex.labor
        )
        * 1000
        * system_data.spec.natural_gas_capacity_mw
        if system_data.spec.nat_gas_type == NaturalGasType.GAS_TURBINE
        else 0
    )
    return gas_turbine_capex_spend


def federal_itc_applicable_spend(
    system_data: SystemData, financial_inputs: FinancialInputs
) -> float:
    """Compute those expenditures which are eligible for the federal investment tax credit."""
    solar_capex = financial_inputs.capex_inputs.solar_capex
    bess_capex = financial_inputs.capex_inputs.bess_capex
    generator_capex = financial_inputs.capex_inputs.generator_capex
    gas_turbine_capex = financial_inputs.capex_inputs.gas_turbine_capex
    system_integration_capex = financial_inputs.capex_inputs.system_integration_capex

    solar_capex_spend_itc_applicable = (
        (
            solar_capex.modules * solar_capex.modules_itc_applicability
            + solar_capex.inverters * solar_capex.inverters_itc_applicability
            + solar_capex.racking_and_foundations
            * solar_capex.racking_and_foundations_itc_applicability
            + solar_capex.balance_of_system
            * solar_capex.balance_of_system_itc_applicability
            + solar_capex.labor * solar_capex.labor_itc_applicability
        )
        * 1000000
        * system_data.spec.solar_capacity_mw
    )
    bess_capex_spend_itc_applicable = (
        (
            bess_capex.bess_units * bess_capex.bess_units_itc_applicability
            + bess_capex.balance_of_system
            * bess_capex.balance_of_system_itc_applicability
            + bess_capex.labor * bess_capex.labor_itc_applicability
        )
        * 1000
        * system_data.spec.bess_energy_capacity_mwh
    )
    generators_capex_spend_itc_applicable = (
        (
            generator_capex.gensets * generator_capex.gensets_itc_applicability
            + generator_capex.balance_of_system
            * generator_capex.balance_of_system_itc_applicability
            + generator_capex.labor * generator_capex.labor_itc_applicability
        )
        * 1000
        * system_data.spec.natural_gas_capacity_mw
        if system_data.spec.nat_gas_type == NaturalGasType.GENERATOR
        else 0
    )
    gas_turbine_capex_spend_itc_applicable = (
        (
            gas_turbine_capex.gas_turbines
            * gas_turbine_capex.gas_turbines_itc_applicability
            + gas_turbine_capex.balance_of_system
            * gas_turbine_capex.balance_of_system_itc_applicability
            + gas_turbine_capex.labor * gas_turbine_capex.labor_itc_applicability
        )
        * 1000
        * system_data.spec.natural_gas_capacity_mw
        if system_data.spec.nat_gas_type == NaturalGasType.GAS_TURBINE
        else 0
    )
    system_integration_capex_spend_itc_applicable = (
        (
            system_integration_capex.microgrid_switchgear_transformers_etc
            * system_integration_capex.microgrid_switchgear_transformers_etc_itc_applicability
            + system_integration_capex.controls
            * system_integration_capex.controls_itc_applicability
            + system_integration_capex.labor
            * system_integration_capex.labor_itc_applicability
        )
        * 1000
        * system_data.spec.load_mw
    )
    hard_capex_spend_itc_applicable = (
        solar_capex_spend_itc_applicable
        + bess_capex_spend_itc_applicable
        + generators_capex_spend_itc_applicable
        + gas_turbine_capex_spend_itc_applicable
        + system_integration_capex_spend_itc_applicable
    )
    total_capex_spend_itc_applicable = hard_capex_spend_itc_applicable * (
        total_capex(system_data, financial_inputs)
        / hard_capex(system_data, financial_inputs)
    )
    return total_capex_spend_itc_applicable


def federal_itc(system_data: SystemData, financial_inputs: FinancialInputs) -> float:
    """Compute the amount of the federal investment tax credit."""
    return (
        federal_itc_applicable_spend(system_data, financial_inputs)
        * financial_inputs.investment_tax_credit
    )


def federal_itc_npv(
    system_data: SystemData, financial_inputs: FinancialInputs
) -> float:
    """Compute the NPV of the federal investment tax credit."""
    annual_federal_itc = [(1, federal_itc(system_data, financial_inputs))]
    return calc_npv(
        annual_federal_itc,
        financial_inputs.cost_of_equity,
        financial_inputs.construction_time,
    )


def debt_service_npv(
    system_data: SystemData, financial_inputs: FinancialInputs
) -> float:
    """Compute the NPV of the debt service payments."""
    starting_balance = (
        total_capex(system_data, financial_inputs) * financial_inputs.leverage
    )
    annual_payment = (
        starting_balance
        * financial_inputs.cost_of_debt
        * ((1 + financial_inputs.cost_of_debt) ** financial_inputs.debt_term)
        / ((1 + financial_inputs.cost_of_debt) ** financial_inputs.debt_term - 1)
    )
    debt_service_payments = []
    for year in range(1, financial_inputs.debt_term + 1):
        debt_service_payments.append((year, -annual_payment))
    return calc_npv(
        debt_service_payments,
        financial_inputs.cost_of_equity,
        financial_inputs.construction_time,
    )


def depreciation_npv(
    system_data: SystemData, financial_inputs: FinancialInputs
) -> float:
    """Compute the NPV of the depreciation."""
    depreciable_amount = -(
        total_capex(system_data, financial_inputs)
        - federal_itc(system_data, financial_inputs) * 0.5
    )
    annual_depreciation = []
    annual_depreciation.append(
        (1, depreciable_amount * financial_inputs.depreciation_yr1)
    )
    annual_depreciation.append(
        (2, depreciable_amount * financial_inputs.depreciation_yr2)
    )
    annual_depreciation.append(
        (3, depreciable_amount * financial_inputs.depreciation_yr3)
    )
    annual_depreciation.append(
        (4, depreciable_amount * financial_inputs.depreciation_yr4)
    )
    annual_depreciation.append(
        (5, depreciable_amount * financial_inputs.depreciation_yr5)
    )
    annual_depreciation.append(
        (6, depreciable_amount * financial_inputs.depreciation_yr6)
    )
    return calc_npv(
        annual_depreciation,
        financial_inputs.cost_of_equity,
        financial_inputs.construction_time,
    )


def interest_expense_npv(
    system_data: SystemData, financial_inputs: FinancialInputs
) -> float:
    """Compute the NPV of the interest expense. This is the interest only, not
    including principal payments as this is needed to calculate tax due.
    """
    starting_balance = (
        total_capex(system_data, financial_inputs) * financial_inputs.leverage
    )
    interest_payments = []
    for year in range(1, financial_inputs.debt_term + 1):
        interest_payment = (
            starting_balance
            * financial_inputs.cost_of_debt
            * (
                (1 + financial_inputs.cost_of_debt) ** financial_inputs.debt_term
                - (1 + financial_inputs.cost_of_debt) ** (year - 1)
            )
            / ((1 + financial_inputs.cost_of_debt) ** financial_inputs.debt_term - 1)
        )
        interest_payments.append((year, -interest_payment))
    return calc_npv(
        interest_payments,
        financial_inputs.cost_of_equity,
        financial_inputs.construction_time,
    )


def tax_benefit_npv(
    system_data: SystemData, financial_inputs: FinancialInputs, lcoe: float
) -> float:
    """Compute the NPV of federal income tax payments including the federal investment tax credit."""
    return -financial_inputs.combined_tax_rate * (
        ebitda_npv(system_data, financial_inputs, lcoe)
        + depreciation_npv(system_data, financial_inputs)
        + interest_expense_npv(system_data, financial_inputs)
    ) + federal_itc_npv(system_data, financial_inputs)


def equity_capex_npv(
    system_data: SystemData, financial_inputs: FinancialInputs
) -> float:
    """Compute the NPV of the capital expenditures funded by equity."""
    total_capex_spend = total_capex(system_data, financial_inputs)
    equity_capex = total_capex_spend * (1 - financial_inputs.leverage)
    equity_capex_per_year = equity_capex / financial_inputs.construction_time
    operating_year_equity_capex = []
    for year in range(0, -financial_inputs.construction_time, -1):
        operating_year_equity_capex.append((year, -equity_capex_per_year))
    return calc_npv(
        operating_year_equity_capex,
        financial_inputs.cost_of_equity,
        financial_inputs.construction_time,
    )


def incremental_after_tax_equity_npv(
    system_data: SystemData, financial_inputs: FinancialInputs
) -> float:
    """Compute the increase in after-tax equity NPV that results from a $1/MWh increase in the LCOE"""
    operating_year_production = []
    for production in system_data.production:
        operating_year_production.append((production.year, production.load_served_mwh))
    production_npv = calc_npv(
        operating_year_production,
        financial_inputs.cost_of_equity,
        financial_inputs.construction_time,
    )
    return production_npv * (1 - financial_inputs.combined_tax_rate)


def breakeven_lcoe(system_data: SystemData, financial_inputs: FinancialInputs) -> float:
    """Computes the LCOE at which the return on equity is equal to the cost of equity and the
    project breaks even. This can be computed directly rather than via a binary search as
    the after-tax equity NPV is linear in the LCOE.
    """
    return -after_tax_equity_npv(
        system_data, financial_inputs, 0
    ) / incremental_after_tax_equity_npv(system_data, financial_inputs)


def lifetime_renewable_percentage(system_data: SystemData) -> float:
    total_load_served_mwh = 0
    total_generator_output_mwh = 0
    for production in system_data.production:
        total_load_served_mwh += production.load_served_mwh
        total_generator_output_mwh += production.generator_output_mwh
    return 1.0 - (total_generator_output_mwh / total_load_served_mwh)


def calc_npv(time_series, discount_rate, year_offset):
    """Helper method to compute a NPV from a series of cash flows. The implementation
    is slightly different than a standard NPV formula as we match the spreadsheet
    in calculating NPV in year -construction_time. This makes sense as for a
    proposed project which has not yet started, this lines up NPV as of the start of
    construction.
    """
    npv = 0
    for entry in time_series:
        npv += entry[1] * (1 + discount_rate) ** (-entry[0] - year_offset)
    return npv


def build_standard_financial_inputs() -> FinancialInputs:
    """Constructs a FinancialInputs proto with baseline values."""
    financial_inputs = FinancialInputs()
    financial_inputs.cost_of_equity = 0.11
    financial_inputs.cost_of_debt = 0.075
    financial_inputs.leverage = 0.70
    financial_inputs.debt_term = 20
    financial_inputs.investment_tax_credit = 0.3
    financial_inputs.construction_time = 2
    financial_inputs.combined_tax_rate = 0.21
    financial_inputs.om_escalator = 0.025
    financial_inputs.fuel_price_mmbtu = 5
    financial_inputs.fuel_escalator = 0.03
    financial_inputs.depreciation_yr1 = 0.20
    financial_inputs.depreciation_yr2 = 0.32
    financial_inputs.depreciation_yr3 = 0.192
    financial_inputs.depreciation_yr4 = 0.115
    financial_inputs.depreciation_yr5 = 0.115
    financial_inputs.depreciation_yr6 = 0.058
    financial_inputs.turbine_vs_generator_fuel_consumption_ratio = 9630.0/8989.3

    financial_inputs.capex_inputs.solar_capex.modules = 0.22
    financial_inputs.capex_inputs.solar_capex.inverters = 0.05
    financial_inputs.capex_inputs.solar_capex.racking_and_foundations = 0.18
    financial_inputs.capex_inputs.solar_capex.balance_of_system = 0.12
    financial_inputs.capex_inputs.solar_capex.labor = 0.20

    financial_inputs.capex_inputs.solar_capex.modules_itc_applicability = 1.0
    financial_inputs.capex_inputs.solar_capex.inverters_itc_applicability = 1.0
    financial_inputs.capex_inputs.solar_capex.racking_and_foundations_itc_applicability = (
        1.0
    )
    financial_inputs.capex_inputs.solar_capex.balance_of_system_itc_applicability = 1.0
    financial_inputs.capex_inputs.solar_capex.labor_itc_applicability = 1.0

    financial_inputs.capex_inputs.bess_capex.bess_units = 200
    financial_inputs.capex_inputs.bess_capex.balance_of_system = 40
    financial_inputs.capex_inputs.bess_capex.labor = 20

    financial_inputs.capex_inputs.bess_capex.bess_units_itc_applicability = 1.0
    financial_inputs.capex_inputs.bess_capex.balance_of_system_itc_applicability = 1.0
    financial_inputs.capex_inputs.bess_capex.labor_itc_applicability = 1.0

    financial_inputs.capex_inputs.generator_capex.gensets = 800
    financial_inputs.capex_inputs.generator_capex.balance_of_system = 200
    financial_inputs.capex_inputs.generator_capex.labor = 150

    financial_inputs.capex_inputs.generator_capex.gensets_itc_applicability = 0
    financial_inputs.capex_inputs.generator_capex.balance_of_system_itc_applicability = (
        0
    )
    financial_inputs.capex_inputs.generator_capex.labor_itc_applicability = 0

    financial_inputs.capex_inputs.gas_turbine_capex.gas_turbines = 635
    financial_inputs.capex_inputs.gas_turbine_capex.balance_of_system = 150
    financial_inputs.capex_inputs.gas_turbine_capex.labor = 100

    financial_inputs.capex_inputs.gas_turbine_capex.gas_turbines_itc_applicability = 0
    financial_inputs.capex_inputs.gas_turbine_capex.balance_of_system_itc_applicability = (
        0
    )
    financial_inputs.capex_inputs.gas_turbine_capex.labor_itc_applicability = 0

    financial_inputs.capex_inputs.system_integration_capex.microgrid_switchgear_transformers_etc = (
        300
    )
    financial_inputs.capex_inputs.system_integration_capex.controls = 50
    financial_inputs.capex_inputs.system_integration_capex.labor = 60

    financial_inputs.capex_inputs.system_integration_capex.microgrid_switchgear_transformers_etc_itc_applicability = (
        0
    )
    financial_inputs.capex_inputs.system_integration_capex.controls_itc_applicability = (
        0
    )
    financial_inputs.capex_inputs.system_integration_capex.labor_itc_applicability = 0

    financial_inputs.capex_inputs.soft_cost_capex.general_conditions = 0.005
    financial_inputs.capex_inputs.soft_cost_capex.epc_overhead = 0.05
    financial_inputs.capex_inputs.soft_cost_capex.design_engineering_and_surveys = 0.005
    financial_inputs.capex_inputs.soft_cost_capex.permitting_and_inspection = 0.0005
    financial_inputs.capex_inputs.soft_cost_capex.startup_and_commissioning = 0.0025
    financial_inputs.capex_inputs.soft_cost_capex.insurance = 0.005
    financial_inputs.capex_inputs.soft_cost_capex.taxes = 0.05

    financial_inputs.opex_inputs.solar_fixed_om_kw = 11.0
    financial_inputs.opex_inputs.bess_fixed_om_kw = 2.5
    financial_inputs.opex_inputs.generators_fixed_om_kw = 10.0
    financial_inputs.opex_inputs.generators_variable_om_kwh = 0.025
    financial_inputs.opex_inputs.gas_turbines_fixed_om_kw = 15.0
    financial_inputs.opex_inputs.gas_turbines_variable_om_kwh = 0.005
    financial_inputs.opex_inputs.bos_fixed_om_kw = 6
    financial_inputs.opex_inputs.soft_costs = 0.0025
    return financial_inputs
