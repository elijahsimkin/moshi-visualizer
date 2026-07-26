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
2. Generate the virtual transactions by running `gen_v_tsx.ipynb`
3. Confirm that `virtual_expenses.csv` and `virtual_income.csv` have been created
### Usage
4. Run `visualize.ipynb`