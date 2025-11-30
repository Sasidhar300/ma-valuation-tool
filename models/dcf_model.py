"""
DCF Valuation Model
Handles all financial calculations for the valuation dashboard
"""

import numpy as np
from typing import List, Dict, Tuple


class DCFModel:
    """Discounted Cash Flow valuation model"""
    
    def __init__(
        self,
        current_revenue: float,
        growth_rates: List[float],
        ebit_margin: float,
        tax_rate: float,
        wacc: float,
        terminal_growth: float,
        fcf_conversion: float = 0.8
    ):
        self.current_revenue = current_revenue
        self.growth_rates = growth_rates
        self.ebit_margin = ebit_margin
        self.tax_rate = tax_rate
        self.wacc = wacc
        self.terminal_growth = terminal_growth
        self.fcf_conversion = fcf_conversion
        
    def project_revenue(self) -> List[float]:
        """Project 5-year revenue based on growth rates"""
        revenues = [self.current_revenue]
        for growth in self.growth_rates:
            revenues.append(revenues[-1] * (1 + growth))
        return revenues[1:]  # Return only projected years (1-5)
    
    def calculate_ebit(self, revenues: List[float]) -> List[float]:
        """Calculate EBIT for each year"""
        return [rev * self.ebit_margin for rev in revenues]
    
    def calculate_nopat(self, ebits: List[float]) -> List[float]:
        """Calculate Net Operating Profit After Tax"""
        return [ebit * (1 - self.tax_rate) for ebit in ebits]
    
    def calculate_fcf(self, nopats: List[float]) -> List[float]:
        """Calculate Free Cash Flow"""
        return [nopat * self.fcf_conversion for nopat in nopats]
    
    def calculate_discount_factors(self) -> List[float]:
        """Calculate discount factors for each year"""
        return [(1 / (1 + self.wacc) ** year) for year in range(1, 6)]
    
    def calculate_pv_fcf(self, fcfs: List[float], discount_factors: List[float]) -> List[float]:
        """Calculate present value of each year's FCF"""
        return [fcf * df for fcf, df in zip(fcfs, discount_factors)]
    
    def calculate_terminal_value(self, final_fcf: float) -> float:
        """Calculate terminal value using perpetuity growth method"""
        return final_fcf * (1 + self.terminal_growth) / (self.wacc - self.terminal_growth)
    
    def calculate_pv_terminal_value(self, terminal_value: float, final_discount_factor: float) -> float:
        """Calculate present value of terminal value"""
        return terminal_value * final_discount_factor
    
    def run_valuation(self) -> Dict:
        """Run complete DCF valuation and return all results"""
        # Project financials
        revenues = self.project_revenue()
        ebits = self.calculate_ebit(revenues)
        nopats = self.calculate_nopat(ebits)
        fcfs = self.calculate_fcf(nopats)
        
        # Calculate present values
        discount_factors = self.calculate_discount_factors()
        pv_fcfs = self.calculate_pv_fcf(fcfs, discount_factors)
        
        # Terminal value
        terminal_value = self.calculate_terminal_value(fcfs[-1])
        pv_terminal_value = self.calculate_pv_terminal_value(terminal_value, discount_factors[-1])
        
        # Enterprise value
        pv_forecast_period = sum(pv_fcfs)
        enterprise_value = pv_forecast_period + pv_terminal_value
        
        return {
            'revenues': revenues,
            'ebits': ebits,
            'nopats': nopats,
            'fcfs': fcfs,
            'discount_factors': discount_factors,
            'pv_fcfs': pv_fcfs,
            'terminal_value': terminal_value,
            'pv_terminal_value': pv_terminal_value,
            'pv_forecast_period': pv_forecast_period,
            'enterprise_value': enterprise_value
        }
    
    def sensitivity_analysis(
        self,
        wacc_range: np.ndarray,
        tg_range: np.ndarray
    ) -> np.ndarray:
        """
        Run sensitivity analysis across WACC and terminal growth combinations
        Returns matrix of enterprise values
        """
        # Pre-calculate FCFs (they don't change with WACC/TG)
        revenues = self.project_revenue()
        ebits = self.calculate_ebit(revenues)
        nopats = self.calculate_nopat(ebits)
        fcfs = self.calculate_fcf(nopats)
        
        sensitivity_matrix = np.zeros((len(tg_range), len(wacc_range)))
        
        for i, tg in enumerate(tg_range):
            for j, w in enumerate(wacc_range):
                # Recalculate with different WACC and terminal growth
                temp_discount_factors = [(1 / (1 + w) ** year) for year in range(1, 6)]
                temp_pv_fcfs = [fcf * df for fcf, df in zip(fcfs, temp_discount_factors)]
                temp_terminal_value = fcfs[-1] * (1 + tg) / (w - tg)
                temp_pv_terminal = temp_terminal_value * temp_discount_factors[-1]
                sensitivity_matrix[i, j] = sum(temp_pv_fcfs) + temp_pv_terminal
        
        return sensitivity_matrix
    
    def calculate_wacc_sensitivity(self) -> Tuple[float, float]:
        """Calculate sensitivity to ±1% change in WACC"""
        results = self.run_valuation()
        base_ev = results['enterprise_value']
        
        # Calculate EV at WACC +1%
        model_plus = DCFModel(
            self.current_revenue, self.growth_rates, self.ebit_margin,
            self.tax_rate, self.wacc + 0.01, self.terminal_growth, self.fcf_conversion
        )
        ev_plus = model_plus.run_valuation()['enterprise_value']
        
        # Calculate EV at WACC -1%
        model_minus = DCFModel(
            self.current_revenue, self.growth_rates, self.ebit_margin,
            self.tax_rate, self.wacc - 0.01, self.terminal_growth, self.fcf_conversion
        )
        ev_minus = model_minus.run_valuation()['enterprise_value']
        
        # Return percentage change
        sensitivity = (ev_minus - ev_plus) / (2 * base_ev)
        return sensitivity, base_ev
