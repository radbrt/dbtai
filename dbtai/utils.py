import yaml
import os
import appdirs
import sqlglot

def get_config():
    configdir = appdirs.user_data_dir("dbtai", "dbtai")

    with open(os.path.join(configdir, "config.yaml"), "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    


def find_ctes(expression, ctes=[]):
    if isinstance(expression, sqlglot.exp.CTE):
        ctes.append(expression)
    if hasattr(expression, "args"):
      for child in expression.args.values():
          if isinstance(child, list):
              for item in child:
                  if hasattr(item, "args"):
                    find_ctes(item, ctes)
          else:
              find_ctes(child, ctes)
    return ctes

def final_selected_columns(sql_query):
    parsed = sqlglot.parse_one(sql_query)
    ctes = find_ctes(parsed)

    columns = [expr.alias_or_name for expr in ctes[-1].this.expressions]
    return columns


parsed = sqlglot.parse_one(sql_query)