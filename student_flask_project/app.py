
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


# ============================================================
# LOAD DATA
# ============================================================

file_path = r"C:\Users\91805\student_data_cleaned.xlsx"

df = pd.read_excel(file_path)


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():

    # --------------------------------------------------------
    # GET FILTER VALUES FROM URL
    # --------------------------------------------------------

    search_name = request.args.get("name", "").strip()

    selected_city = request.args.get("city", "")

    selected_state = request.args.get("state", "")

    selected_certificate = request.args.get(
        "certificate", ""
    )


    # --------------------------------------------------------
    # CREATE FILTERED DATA
    # --------------------------------------------------------

    filtered_df = df.copy()


    # Student Name filter

    if search_name:

        filtered_df = filtered_df[
            filtered_df["Student Name"]
            .astype(str)
            .str.contains(
                search_name,
                case=False,
                na=False
            )
        ]


    # City filter

    if selected_city:

        filtered_df = filtered_df[
            filtered_df["City"] == selected_city
        ]


    # State filter

    if selected_state:

        filtered_df = filtered_df[
            filtered_df["State"] == selected_state
        ]


    # Certificate filter

    if selected_certificate:

        filtered_df = filtered_df[
            filtered_df["Issued Certificate"]
            == selected_certificate
        ]


    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_students = len(filtered_df)


    if total_students > 0:

        average_age = round(
            filtered_df["Age"].mean(),
            1
        )

        minimum_age = int(
            filtered_df["Age"].min()
        )

        maximum_age = int(
            filtered_df["Age"].max()
        )

    else:

        average_age = 0
        minimum_age = 0
        maximum_age = 0


    # --------------------------------------------------------
    # CITY DATA
    # --------------------------------------------------------

    city_data = (
        filtered_df["City"]
        .value_counts()
        .to_dict()
    )


    # --------------------------------------------------------
    # STATE DATA
    # --------------------------------------------------------

    state_data = (
        filtered_df["State"]
        .value_counts()
        .to_dict()
    )


    # --------------------------------------------------------
    # CERTIFICATE DATA
    # --------------------------------------------------------

    certificate_data = (
        filtered_df["Issued Certificate"]
        .value_counts()
        .to_dict()
    )


    # --------------------------------------------------------
    # AGE GROUP
    # --------------------------------------------------------

    filtered_df["Age Group"] = pd.cut(

        filtered_df["Age"],

        bins=[0, 18, 25, 35, 45, 60, 100],

        labels=[
            "Below 18",
            "18-25",
            "26-35",
            "36-45",
            "46-60",
            "Above 60"
        ]
    )


    age_group_data = (

        filtered_df["Age Group"]

        .value_counts()

        .sort_index()

        .to_dict()
    )


    # --------------------------------------------------------
    # FILTER OPTIONS
    # --------------------------------------------------------

    cities = sorted(
        df["City"]
        .dropna()
        .unique()
        .tolist()
    )


    states = sorted(
        df["State"]
        .dropna()
        .unique()
        .tolist()
    )


    certificates = sorted(
        df["Issued Certificate"]
        .dropna()
        .unique()
        .tolist()
    )


    # --------------------------------------------------------
    # STUDENT TABLE
    # --------------------------------------------------------

    table_df = filtered_df[
        [
            "Student Name",
            "Age",
            "Contact Number",
            "Email ID",
            "City",
            "State",
            "Issued Certificate"
        ]
    ].copy()


    # Limit table to first 100 records

    table_df = table_df.head(100)


    students = table_df.to_dict(
        orient="records"
    )


    # --------------------------------------------------------
    # SEND DATA TO HTML
    # --------------------------------------------------------

    return render_template(

        "index.html",

        total_students=total_students,

        average_age=average_age,

        minimum_age=minimum_age,

        maximum_age=maximum_age,

        city_data=city_data,

        state_data=state_data,

        certificate_data=certificate_data,

        age_group_data=age_group_data,

        cities=cities,

        states=states,

        certificates=certificates,

        students=students,

        search_name=search_name,

        selected_city=selected_city,

        selected_state=selected_state,

        selected_certificate=selected_certificate
    )


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=False,
        use_reloader=False
    )
