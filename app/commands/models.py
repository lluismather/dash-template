
def model__make(ctx, model_name, table_name):
    """Create a new model file with a given name."""
    if not model_name:
        raise ValueError("Model name cannot be empty")
    if not table_name:
        raise ValueError("Table name cannot be empty")

    model_file = f"app/models/{table_name}.py"

    with open(model_file, "w") as f:
        f.write(f"\n")
        f.write(f"from app.providers.app_provider import db\n")
        f.write(f"\n")
        f.write(f"\n")
        f.write(f"class {model_name}(db.Model):\n")
        f.write(f"    __tablename__ = \"{table_name}\"\n")
        f.write(f"    id = db.Column(db.Integer, primary_key=True)\n")
        f.write(f"    created_at = db.Column(db.DateTime, server_default=db.func.now())\n")
        f.write(f"    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())\n")
        f.write(f"\n")
        f.write(f"    def __repr__(self):\n")
        f.write(f"        return f\"<{model_name} {{self.id}}>\"\n")
        f.write(f"\n")

    print(f"Model created at {model_file}")
model__make.args = [
    ("model_name", {"type": str, "help": "Model name"}),
    ("table_name", {"type": str, "help": "Table name"}),
]
