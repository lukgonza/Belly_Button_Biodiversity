{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import Dependencies\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, jsonify, render_template\n",
    "from flask_sqlalchemy import SQLAlchemy"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\lukgo\\Anaconda3\\lib\\site-packages\\flask_sqlalchemy\\__init__.py:794: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.\n",
      "  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '\n"
     ]
    }
   ],
   "source": [
    "app.config[\"SQLALCHEMY_DATABASE_URI\"] = \"sqlite:///db/bellybutton.sqlite\"\n",
    "db = SQLAlchemy(app)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(db.engine, reflect=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save references to each table\n",
    "Samples_Metadata = Base.classes.sample_metadata\n",
    "Samples = Base.classes.samples"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/\")\n",
    "def index():\n",
    "    \"\"\"Return the homepage.\"\"\"\n",
    "    return render_template(\"index.html\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/names\")\n",
    "def names():\n",
    "    \"\"\"Return a list of sample names.\"\"\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    " # Use Pandas to perform the sql query\n",
    "    stmt = db.session.query(Samples).statement\n",
    "    df = pd.read_sql_query(stmt, db.session.bind)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Return a list of the column names (sample names)\n",
    "    return jsonify(list(df.columns)[2:])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/metadata/<sample>\")\n",
    "def sample_metadata(sample):\n",
    "    \"\"\"Return the MetaData for a given sample.\"\"\"\n",
    "    sel = [\n",
    "        Samples_Metadata.sample,\n",
    "        Samples_Metadata.ETHNICITY,\n",
    "        Samples_Metadata.GENDER,\n",
    "        Samples_Metadata.AGE,\n",
    "        Samples_Metadata.LOCATION,\n",
    "        Samples_Metadata.BBTYPE,\n",
    "        Samples_Metadata.WFREQ,\n",
    "    ]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    " results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    " # Create a dictionary entry for each row of metadata information\n",
    "    sample_metadata = {}\n",
    "    for result in results:\n",
    "        sample_metadata[\"sample\"] = result[0]\n",
    "        sample_metadata[\"ETHNICITY\"] = result[1]\n",
    "        sample_metadata[\"GENDER\"] = result[2]\n",
    "        sample_metadata[\"AGE\"] = result[3]\n",
    "        sample_metadata[\"LOCATION\"] = result[4]\n",
    "        sample_metadata[\"BBTYPE\"] = result[5]\n",
    "        sample_metadata[\"WFREQ\"] = result[6]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(sample_metadata)\n",
    "    return jsonify(sample_metadata)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/samples/<sample>\")\n",
    "def samples(sample):\n",
    "    \"\"\"Return `otu_ids`, `otu_labels`,and `sample_values`.\"\"\"\n",
    "    stmt = db.session.query(Samples).statement\n",
    "    df = pd.read_sql_query(stmt, db.session.bind)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Filter the data based on the sample number and\n",
    "    # only keep rows with values above 1\n",
    "    sample_data = df.loc[df[sample] > 1, [\"otu_id\", \"otu_label\", sample]]\n",
    "    # Format the data to send as json\n",
    "    data = {\n",
    "        \"otu_ids\": sample_data.otu_id.values.tolist(),\n",
    "        \"sample_values\": sample_data[sample].values.tolist(),\n",
    "        \"otu_labels\": sample_data.otu_label.tolist(),\n",
    "    }\n",
    "    return jsonify(data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "if __name__ == \"__main__\":\n",
    "    # Bind to PORT if defined, otherwise default to 5000.\n",
    "    port = int(os.environ.get('PORT', 5000))\n",
    "    app.run(host='0.0.0.0', port=port)\n",
    "    # app.run()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
