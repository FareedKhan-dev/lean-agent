from _hidden_kit import check, load, report

handlers = load("shopfront.api.handlers")
load("shopfront.data").load_demo()
service = handlers.SERVICES.customers
correct = check("found in any case", lambda: service.find_by_email("ANN@example.org").id == 1
                and service.find_by_email("bo@example.org").id == 2 and service.find_by_email("x@example.org") is None)
report(correct)
