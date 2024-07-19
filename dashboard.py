from vizro import Vizro
import vizro.plotly.express as px
import vizro.models as vm
from vizro.managers import data_manager
from vizro.tables import dash_ag_grid
import duckdb

con = duckdb.connect("data/hafen-hamburg-de/db.duckdb", read_only=True)


def load_container_data():
    return con.execute("SELECT * FROM containerhandling").fetchdf()


def load_seaborne_cargo_data():
    return con.execute("SELECT * FROM seabornecargohandling").fetchdf()


data_manager["container_data"] = load_container_data
data_manager["seaborne_cargo_data"] = load_seaborne_cargo_data


def control_year():
    return vm.Filter(column="year", selector=vm.RangeSlider(step=1, marks=None))


pagination_options = {"pagination": True, "paginationPageSize": 10, "paginationPageSizeSelector": False}

page_container_chart_import_export = vm.Page(
    title="Import vs Export",
    components=[
        vm.Graph(id="bar_container_import_export", figure=px.bar("container_data", x="year", y=["import", "export"], barmode="group")),
    ],
    controls=[control_year()]
)

page_container_chart_full_empty = vm.Page(
    title="Filled vs Empty",
    components=[
        vm.Graph(id="bar_container_filled_empty", figure=px.bar("container_data", x="year", y=["full", "empty"], barmode="group")),
    ],
    controls=[control_year()]
)

page_container_table = vm.Page(
    title="Container Handling Table",
    components=[
        vm.AgGrid(figure=dash_ag_grid(data_frame="container_data", dashGridOptions={**pagination_options}))
    ],
)

page_seaborne_cargo_charts = vm.Page(
    title="Seaborne Cargo Charts",
    components=[
        vm.Graph(id="bar_import", figure=px.bar("seaborne_cargo_data", title="Import", x="year", y=["seaborne_import", "bulk_import"], barmode="group")),
        vm.Graph(id="bar_export", figure=px.bar("seaborne_cargo_data", title="Export", x="year", y=["seaborne_export", "bulk_export"], barmode="group")),
    ],
    controls=[control_year()]
)

page_seaborne_cargo_table = vm.Page(
    title="Seaborne Cargo Table",
    components=[
        vm.AgGrid(figure=dash_ag_grid(data_frame="seaborne_cargo_data", dashGridOptions={**pagination_options}))
    ],
)

dashboard = Vizro().build(
    vm.Dashboard(
        title="Hafen Hamburg",
        pages=[
            page_container_chart_import_export,
            page_container_chart_full_empty,
            page_container_table,
            page_seaborne_cargo_charts,
            page_seaborne_cargo_table
        ],
        navigation=vm.Navigation(pages={
            "Container Handling": [
                page_container_chart_import_export.id,
                page_container_chart_full_empty.id,
                page_container_table.id
            ],
            "Seaborne Cargo Handling": [
                page_seaborne_cargo_charts.id,
                page_seaborne_cargo_table.id
            ]
        }),
    )
)  

if __name__ == "__main__":  
    dashboard.run(host="0.0.0.0", port=80)
    # dashboard.run(debug=True)
