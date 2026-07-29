# This file contains the helper functions for visualize.ipynb

def add_vacc_nodes(layer, vaccs = ['Tuition', 'Groceries', 'Rent', 'Lease', 'Insurance', 'Free Cash']):
	for node in sorted(vaccs,reverse=True): 
		layer.add_node(node)

def link_rincs_to_raccs(ri, ra, income_amount_by_source, inc_colors):
    for income_source in income_amount_by_source.iterrows():
        from_via, amount_series = income_source
        frm, via = from_via
        amount = amount_series['amount']

        color = inc_colors[frm]

        ri.get_node(frm).connect_to(
                ra.get_node(via), 
		weight=amount,
                color=color
	)
def link_raccs_to_vaccs(ra, va, inc_cashflow, inc_colors):
    # from,     via,       to,          amount
    # AECOM,    Checking,  Free Cash,   $500
    for tx in inc_cashflow.iterrows():
        cash_path, amount_series = tx
        amount = amount_series['amount']
        frm, via, to = cash_path
        color = inc_colors[frm]

        ra.get_node(via).connect_to(
                va.get_node(to), 
		weight=amount,
                color=color
        )

def link_vaccs_to_raccouts(va, raa, vacc_to_raccouts_amts, vacc_colors):
	for from_via_amount in vacc_to_raccouts_amts.iterrows():
		from_via, amt_series = from_via_amount
		amt = amt_series['amount']
		frm, via = from_via
		try:	
			va.get_node(frm).connect_to(
				raa.get_node(via), 
				weight=amt, 
				color=vacc_colors[frm]
			)
		except: pass
def link_raccouts_to_routs(raa, ro, out_cashflow_txs, vacc_colors):
	for from_via_to_amt in out_cashflow_txs.iterrows():
		from_via_to, amt_series = from_via_to_amt
		amt = amt_series['amount']
		frm, via, to = from_via_to
		try:
			raa.get_node(via).connect_to(
				ro.get_node(to),
				weight=amt,
				color=vacc_colors[frm]
			)
		except:
			print(f'Exception on {frm,via,to,amt}'  )
		
def add_rinc_nodes(ri, income_txs):
    for frm in set(income_txs['from']):
        ri.add_node(frm)

def add_racc_nodes(ra, income_txs):
    for to in set(income_txs['to']):
        ra.add_node(to)

def add_raccout_nodes(raa,real_outflow_txs):
    for frm in set(real_outflow_txs['from']):
        raa.add_node(frm)

def add_rout_nodes(ro, real_outflow_txs):
    for to in set(real_outflow_txs['to']):
        ro.add_node(to)
import pandas as pd