#  Copyright 2019-2020 The Lux Authors.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from lux.vislib.altair.AltairChart import AltairChart
import altair as alt

alt.data_transformers.disable_max_rows()
from lux.utils.utils import get_agg_title


class LineChart(AltairChart):
    """
    LineChart is a subclass of AltairChart that render as a line charts.
    All rendering properties for line charts are set here.

    See Also
    --------
    altair-viz.github.io
    """

    def __init__(self, dobj):
        super().__init__(dobj)

    def __repr__(self):
        return f"Line Chart <{str(self.vis)}>"

    def initialize_chart(self):
        self.tooltip = False  # tooltip looks weird for line chart
        x_attr = self.vis.get_attr_by_channel("x")[0]
        y_attr = self.vis.get_attr_by_channel("y")[0]

        x_attr_abv = x_attr.attribute
        y_attr_abv = y_attr.attribute

        if len(x_attr.attribute) > 25:
            x_attr_abv = x_attr.attribute[:15] + "..." + x_attr.attribute[-10:]
        if len(y_attr.attribute) > 25:
            y_attr_abv = y_attr.attribute[:15] + "..." + y_attr.attribute[-10:]

        x_attr.attribute = x_attr.attribute.replace(".", "")
        y_attr.attribute = y_attr.attribute.replace(".", "")

        # Remove NaNs only for Line Charts (offsets axis range)
        self.data = self.data.dropna(subset=[x_attr.attribute, y_attr.attribute])
        self.code += "import altair as alt\n"
        self.code += "import pandas._libs.tslibs.timestamps\n"
        self.code += "from pandas._libs.tslibs.timestamps import Timestamp\n"
        self.code += f"visData = pd.DataFrame({str(self.data.to_dict())})\n"

        if y_attr.data_model == "measure":
            agg_title = get_agg_title(y_attr)
            x_attr_spec = alt.X(x_attr.attribute, type=x_attr.data_type, axis=alt.Axis(title=x_attr_abv))
            y_attr_spec = alt.Y(
                y_attr.attribute, type=y_attr.data_type, title=agg_title, axis=alt.Axis(title=y_attr_abv)
            )
            x_attr_field_code = f"alt.X('{x_attr.attribute}', type = '{x_attr.data_type}', axis=alt.Axis(title='{x_attr_abv}'))"
            y_attr_fieldCode = f"alt.Y('{y_attr.attribute}', type= '{y_attr.data_type}', title='{agg_title}', axis=alt.Axis(title='{y_attr_abv}')"
        else:
            agg_title = get_agg_title(x_attr)
            x_attr_spec = alt.X(
                x_attr.attribute, type=x_attr.data_type, title=agg_title, axis=alt.Axis(title=x_attr_abv)
            )
            y_attr_spec = alt.Y(y_attr.attribute, type=y_attr.data_type, axis=alt.Axis(title=y_attr_abv))
            x_attr_field_code = f"alt.X('{x_attr.attribute}', type = '{x_attr.data_type}', title='{agg_title}', axis=alt.Axis(title='{x_attr_abv}')"
            y_attr_fieldCode = f"alt.Y('{y_attr.attribute}', type= '{y_attr.data_type}', axis=alt.Axis(title='{u_attr_abv}')"

        chart = alt.Chart(self.data).mark_line().encode(x=x_attr_spec, y=y_attr_spec)
        chart = chart.interactive()  # Enable Zooming and Panning
        self.code += f"""
		chart = alt.Chart(visData).mark_line().encode(
		    y = {y_attr_fieldCode},
		    x = {x_attr_field_code},
		)
		chart = chart.interactive() # Enable Zooming and Panning
		"""
        return chart
