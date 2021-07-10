from datetime import datetime
from typing import Optional, List, Set, Any
from dataclasses import dataclass
import logging
from nmdc_schema.nmdc import QuantityValue
import re
#import pint
from quantulum3 import parser as q_parser
from quantulum3.classes import Quantity

from sample_annotator.report_model import AnnotationReport

LoQ = List[Quantity]

@dataclass
class MeasurementEngine():


    def repair(self, measurement_verbatim: Any, default_unit: str = None, report: AnnotationReport = None) -> QuantityValue:
        """
        Repair a measurement field

        Example: '2cm'
        """
        m: LoQ
        if isinstance(measurement_verbatim, QuantityValue):
            qv = measurement_verbatim
            if qv.has_unit is None and qv.has_numeric_value is None:
                measurement_verbatim = qv.has_raw_value
            else:
                report.add_message(f'Incomplete info: {qv}')
                measurement_verbatim = qv.has_raw_value
        if isinstance(measurement_verbatim, int) or isinstance(measurement_verbatim, float):
            if default_unit is None:
                report.add_message(f'Missing unit {measurement_verbatim}')
            else:
                report.add_message(f'Adding default unit {measurement_verbatim} => {default_unit}',
                                   was_repaired=True)
            return QuantityValue(has_unit=default_unit,
                                 has_numeric_value=measurement_verbatim,
                                 has_raw_value=str(measurement_verbatim))
        m = q_parser.parse(measurement_verbatim)
        if len(m) == 0:
            return None
        q = m[0]
        report.add_message(f'Parsed unit-value: {q.value} {q.unit.name}')
        return QuantityValue(has_unit=q.unit.name,
                             has_numeric_value=q.value,
                             has_raw_value=measurement_verbatim)


