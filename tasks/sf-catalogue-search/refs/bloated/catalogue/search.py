from dataclasses import dataclass, field


@dataclass
class Query:
    table: str
    columns: list
    conditions: list = field(default_factory=list)
    params: list = field(default_factory=list)
    order_by: str = ""

    def where(self, condition, *params):
        self.conditions.append(condition)
        self.params.extend(params)
        return self

    def order(self, column):
        self.order_by = column
        return self

    def sql(self):
        text = f"SELECT {', '.join(self.columns)} FROM {self.table}"
        if self.conditions:
            text += " WHERE " + " AND ".join(self.conditions)
        if self.order_by:
            text += f" ORDER BY {self.order_by}"
        return text


class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def run(self, query):
        return self.conn.execute(query.sql(), query.params).fetchall()


class ProductSearchService:
    def __init__(self, conn):
        self.repository = ProductRepository(conn)

    def search(self, term):
        query = Query("products", ["name"]).where("name LIKE ?", f"%{term}%").order("name")
        return [name for (name,) in self.repository.run(query)]


def search_products(conn, term):
    """Names of products whose name contains `term`, ignoring case, sorted by name."""
    return ProductSearchService(conn).search(term)
