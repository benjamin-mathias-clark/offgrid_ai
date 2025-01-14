# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: offgrid_ai.proto
# Protobuf Python Version: 5.29.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    2,
    '',
    'offgrid_ai.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10offgrid_ai.proto\x12\noffgrid_ai\"7\n\x08\x44\x61taFile\x12+\n\x0bsystem_data\x18\x01 \x03(\x0b\x32\x16.offgrid_ai.SystemData\"d\n\nSystemData\x12$\n\x04spec\x18\x01 \x01(\x0b\x32\x16.offgrid_ai.SystemSpec\x12\x30\n\nproduction\x18\x02 \x03(\x0b\x32\x1c.offgrid_ai.SystemProduction\"\xda\x01\n\nSystemSpec\x12\x10\n\x08location\x18\x01 \x01(\t\x12\x0f\n\x07load_mw\x18\x02 \x01(\x01\x12\x19\n\x11solar_capacity_mw\x18\x03 \x01(\x01\x12\x19\n\x11\x62\x65ss_max_power_mw\x18\x04 \x01(\x01\x12 \n\x18\x62\x65ss_energy_capacity_mwh\x18\x05 \x01(\x01\x12\x1f\n\x17natural_gas_capacity_mw\x18\x06 \x01(\x01\x12\x30\n\x0cnat_gas_type\x18\x07 \x01(\x0e\x32\x1a.offgrid_ai.NaturalGasType\"\xeb\x01\n\x10SystemProduction\x12\x0c\n\x04year\x18\x01 \x01(\x05\x12\x1c\n\x14solar_output_raw_mwh\x18\x02 \x01(\x01\x12\x1c\n\x14solar_output_net_mwh\x18\x03 \x01(\x01\x12\x1b\n\x13\x62\x65ss_throughput_mwh\x18\x04 \x01(\x01\x12\x1b\n\x13\x62\x65ss_net_output_mwh\x18\x05 \x01(\x01\x12\x1c\n\x14generator_output_mwh\x18\x06 \x01(\x01\x12\x1c\n\x14generator_fuel_mmbtu\x18\x07 \x01(\x01\x12\x17\n\x0fload_served_mwh\x18\x08 \x01(\x01\"\xc6\x04\n\x0f\x46inancialInputs\x12\x16\n\x0e\x63ost_of_equity\x18\x01 \x01(\x01\x12\x14\n\x0c\x63ost_of_debt\x18\x02 \x01(\x01\x12\x10\n\x08leverage\x18\x03 \x01(\x01\x12\x11\n\tdebt_term\x18\x04 \x01(\x05\x12\x1d\n\x15investment_tax_credit\x18\x05 \x01(\x01\x12\x19\n\x11\x63onstruction_time\x18\x06 \x01(\x05\x12\x19\n\x11\x63ombined_tax_rate\x18\x07 \x01(\x01\x12\x14\n\x0com_escalator\x18\x08 \x01(\x01\x12\x18\n\x10\x66uel_price_mmbtu\x18\t \x01(\x01\x12\x16\n\x0e\x66uel_escalator\x18\n \x01(\x01\x12\x18\n\x10\x64\x65preciation_yr1\x18\x0b \x01(\x01\x12\x18\n\x10\x64\x65preciation_yr2\x18\x0c \x01(\x01\x12\x18\n\x10\x64\x65preciation_yr3\x18\r \x01(\x01\x12\x18\n\x10\x64\x65preciation_yr4\x18\x0e \x01(\x01\x12\x18\n\x10\x64\x65preciation_yr5\x18\x0f \x01(\x01\x12\x18\n\x10\x64\x65preciation_yr6\x18\x10 \x01(\x01\x12-\n\x0c\x63\x61pex_inputs\x18\x11 \x01(\x0b\x32\x17.offgrid_ai.CapexInputs\x12+\n\x0bopex_inputs\x18\x12 \x01(\x0b\x32\x16.offgrid_ai.OpexInputs\x12\x33\n+turbine_vs_generator_fuel_consumption_ratio\x18\x13 \x01(\x01\x12\x16\n\x0elcoe_escalator\x18\x14 \x01(\x01\"\xb1\x0e\n\x0b\x43\x61pexInputs\x12=\n\x0bsolar_capex\x18\x01 \x01(\x0b\x32(.offgrid_ai.CapexInputs.SolarCapexInputs\x12;\n\nbess_capex\x18\x02 \x01(\x0b\x32\'.offgrid_ai.CapexInputs.BessCapexInputs\x12\x45\n\x0fgenerator_capex\x18\x03 \x01(\x0b\x32,.offgrid_ai.CapexInputs.GeneratorCapexInputs\x12H\n\x11gas_turbine_capex\x18\x04 \x01(\x0b\x32-.offgrid_ai.CapexInputs.GasTurbineCapexInputs\x12V\n\x18system_integration_capex\x18\x05 \x01(\x0b\x32\x34.offgrid_ai.CapexInputs.SystemIntegrationCapexInputs\x12\x44\n\x0fsoft_cost_capex\x18\x06 \x01(\x0b\x32+.offgrid_ai.CapexInputs.SoftCostCapexInputs\x1a\xca\x02\n\x10SolarCapexInputs\x12\x0f\n\x07modules\x18\x01 \x01(\x01\x12\x11\n\tinverters\x18\x02 \x01(\x01\x12\x1f\n\x17racking_and_foundations\x18\x03 \x01(\x01\x12\x19\n\x11\x62\x61lance_of_system\x18\x04 \x01(\x01\x12\r\n\x05labor\x18\x05 \x01(\x01\x12!\n\x19modules_itc_applicability\x18\x06 \x01(\x01\x12#\n\x1binverters_itc_applicability\x18\x07 \x01(\x01\x12\x31\n)racking_and_foundations_itc_applicability\x18\x08 \x01(\x01\x12+\n#balance_of_system_itc_applicability\x18\t \x01(\x01\x12\x1f\n\x17labor_itc_applicability\x18\n \x01(\x01\x1a\xc3\x01\n\x0f\x42\x65ssCapexInputs\x12\x12\n\nbess_units\x18\x01 \x01(\x01\x12\x19\n\x11\x62\x61lance_of_system\x18\x02 \x01(\x01\x12\r\n\x05labor\x18\x03 \x01(\x01\x12$\n\x1c\x62\x65ss_units_itc_applicability\x18\x04 \x01(\x01\x12+\n#balance_of_system_itc_applicability\x18\x05 \x01(\x01\x12\x1f\n\x17labor_itc_applicability\x18\x06 \x01(\x01\x1a\xc2\x01\n\x14GeneratorCapexInputs\x12\x0f\n\x07gensets\x18\x01 \x01(\x01\x12\x19\n\x11\x62\x61lance_of_system\x18\x02 \x01(\x01\x12\r\n\x05labor\x18\x03 \x01(\x01\x12!\n\x19gensets_itc_applicability\x18\x04 \x01(\x01\x12+\n#balance_of_system_itc_applicability\x18\x05 \x01(\x01\x12\x1f\n\x17labor_itc_applicability\x18\x06 \x01(\x01\x1a\xcd\x01\n\x15GasTurbineCapexInputs\x12\x14\n\x0cgas_turbines\x18\x01 \x01(\x01\x12\x19\n\x11\x62\x61lance_of_system\x18\x02 \x01(\x01\x12\r\n\x05labor\x18\x03 \x01(\x01\x12&\n\x1egas_turbines_itc_applicability\x18\x04 \x01(\x01\x12+\n#balance_of_system_itc_applicability\x18\x05 \x01(\x01\x12\x1f\n\x17labor_itc_applicability\x18\x06 \x01(\x01\x1a\xf4\x01\n\x1cSystemIntegrationCapexInputs\x12-\n%microgrid_switchgear_transformers_etc\x18\x01 \x01(\x01\x12\x10\n\x08\x63ontrols\x18\x02 \x01(\x01\x12\r\n\x05labor\x18\x03 \x01(\x01\x12?\n7microgrid_switchgear_transformers_etc_itc_applicability\x18\x04 \x01(\x01\x12\"\n\x1a\x63ontrols_itc_applicability\x18\x05 \x01(\x01\x12\x1f\n\x17labor_itc_applicability\x18\x06 \x01(\x01\x1a\xd7\x01\n\x13SoftCostCapexInputs\x12\x1a\n\x12general_conditions\x18\x01 \x01(\x01\x12\x14\n\x0c\x65pc_overhead\x18\x02 \x01(\x01\x12&\n\x1e\x64\x65sign_engineering_and_surveys\x18\x03 \x01(\x01\x12!\n\x19permitting_and_inspection\x18\x04 \x01(\x01\x12!\n\x19startup_and_commissioning\x18\x05 \x01(\x01\x12\x11\n\tinsurance\x18\x06 \x01(\x01\x12\r\n\x05taxes\x18\x07 \x01(\x01\"\xfa\x01\n\nOpexInputs\x12\x19\n\x11solar_fixed_om_kw\x18\x01 \x01(\x01\x12\x18\n\x10\x62\x65ss_fixed_om_kw\x18\x02 \x01(\x01\x12\x1e\n\x16generators_fixed_om_kw\x18\x03 \x01(\x01\x12\"\n\x1agenerators_variable_om_kwh\x18\x04 \x01(\x01\x12 \n\x18gas_turbines_fixed_om_kw\x18\x05 \x01(\x01\x12$\n\x1cgas_turbines_variable_om_kwh\x18\x06 \x01(\x01\x12\x17\n\x0f\x62os_fixed_om_kw\x18\x07 \x01(\x01\x12\x12\n\nsoft_costs\x18\x08 \x01(\x01*0\n\x0eNaturalGasType\x12\r\n\tGENERATOR\x10\x01\x12\x0f\n\x0bGAS_TURBINE\x10\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'offgrid_ai_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_NATURALGASTYPE']._serialized_start=3332
  _globals['_NATURALGASTYPE']._serialized_end=3380
  _globals['_DATAFILE']._serialized_start=32
  _globals['_DATAFILE']._serialized_end=87
  _globals['_SYSTEMDATA']._serialized_start=89
  _globals['_SYSTEMDATA']._serialized_end=189
  _globals['_SYSTEMSPEC']._serialized_start=192
  _globals['_SYSTEMSPEC']._serialized_end=410
  _globals['_SYSTEMPRODUCTION']._serialized_start=413
  _globals['_SYSTEMPRODUCTION']._serialized_end=648
  _globals['_FINANCIALINPUTS']._serialized_start=651
  _globals['_FINANCIALINPUTS']._serialized_end=1233
  _globals['_CAPEXINPUTS']._serialized_start=1236
  _globals['_CAPEXINPUTS']._serialized_end=3077
  _globals['_CAPEXINPUTS_SOLARCAPEXINPUTS']._serialized_start=1679
  _globals['_CAPEXINPUTS_SOLARCAPEXINPUTS']._serialized_end=2009
  _globals['_CAPEXINPUTS_BESSCAPEXINPUTS']._serialized_start=2012
  _globals['_CAPEXINPUTS_BESSCAPEXINPUTS']._serialized_end=2207
  _globals['_CAPEXINPUTS_GENERATORCAPEXINPUTS']._serialized_start=2210
  _globals['_CAPEXINPUTS_GENERATORCAPEXINPUTS']._serialized_end=2404
  _globals['_CAPEXINPUTS_GASTURBINECAPEXINPUTS']._serialized_start=2407
  _globals['_CAPEXINPUTS_GASTURBINECAPEXINPUTS']._serialized_end=2612
  _globals['_CAPEXINPUTS_SYSTEMINTEGRATIONCAPEXINPUTS']._serialized_start=2615
  _globals['_CAPEXINPUTS_SYSTEMINTEGRATIONCAPEXINPUTS']._serialized_end=2859
  _globals['_CAPEXINPUTS_SOFTCOSTCAPEXINPUTS']._serialized_start=2862
  _globals['_CAPEXINPUTS_SOFTCOSTCAPEXINPUTS']._serialized_end=3077
  _globals['_OPEXINPUTS']._serialized_start=3080
  _globals['_OPEXINPUTS']._serialized_end=3330
# @@protoc_insertion_point(module_scope)
