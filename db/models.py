from dataclasses import dataclass, field


@dataclass
class LayerModel:
    """
    Use this class to declare database tables
    """
    table_name: str
    geom_column: str = "geom"
    layer_column: str = None
    include_columns: list = field(default_factory=list)

    def __post_init__(self):
        if self.layer_column:
            self.sql_layer = self.layer_column + " AS layer"
        else:
            self.sql_layer = self.table_name + "_layer AS layer"
        if self.include_columns:
            self.sql_columns = ", ".join(self.include_columns) + ","
        else:
            self.sql_columns = ""


ExampleLayer = LayerModel(
    table_name="boundaries",
    layer_column="layer",
    include_columns=["name", "population"]
)
