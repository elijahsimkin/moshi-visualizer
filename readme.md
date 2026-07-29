<br />
<div align="center">
<img src="docs/logo.png" alt="Logo" width="80" height="80">

  <h3 align="center">Moshi Flow Chart</h3>

  <p align="center">
    A Project for visualizing real => virtual cashflows.
 </p>
</div>

---

## About The Project
This is a visualizer for cash flows between real and virtual accounts. It visualizes cash flow as thick arrows that flow from real income accounts into real user accounts, and from there into virtual accounts, out of the virtual accounts and into the real user accounts and from the real user accounts into the foreign expense accounts.

![An example flow chart](/docs/example_chart.png)

## Getting Started
### Prerequisites
1. Install dependencies
`pip install pandas matplotlib`
2. Run `visualize.ipynb`
### Visualizing Your Own Dataj
The real and virtual expenses have already been created. If you want to run it on your own data
  1. Create a new `toy_data_#` folder (this is your `data_folder`!) in `data/`. For example `toy_data_4`

  2. Create a `real_expenses.csv` and a `real_income.csv` file according to the schema `txid,from,to,amount`
    * `txid` is the transaction id, 
    * `from` is the "real" account it is coming from and 
    * `to` is the real account it going to. 
    * `amount` is the amount that is being moved in dollars

  3. Create a `virtual_expenses.csv` and a `virtual_income.csv` file according to the schema `vtxid,txid,from,to,amount`, where 
    * `vtxid` is the virtual transaction id, 
    * `txid` is the transaction id that it is derived from, 
    * `from` is the "real" account it is coming from and 
    * `to` is the real account it going to. 
    * `amount` is the amount that is being moved in dollars
  4. To run the visualizer, in `visualize.ipynb` use search for `SETUP CUSTOM_VACCS` and do

    setup.add_vacc_nodes(va, vaccs=['VA1', 'VA2', ..., 'VAN])

  Where 'VA1', ... etc are your custom virtual accounts

  5. In `visualize.ipynb` set `data_folder` at the top `=` to the data_folder name you selected above.